import torch
from torch import nn
from transformers import RobertaModel, HubertModel, AutoModel, Data2VecAudioModel
from utils.cross_attn_encoder import CMELayer, BertConfig
import torch.nn.functional as F



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# English text model + context
class roberta_en_context(nn.Module):
            
    def __init__(self):        
        super().__init__() 
        self.roberta_model = AutoModel.from_pretrained('./models/roberta-large', local_files_only=True) # with context, we can improve using a larger model
        self.classifier = nn.Linear(1024*2, 1)    
   
    def forward(self, input_ids, attention_mask, context_input_ids, context_attention_mask):        
        raw_output = self.roberta_model(input_ids, attention_mask, return_dict=True)        
        input_pooler = raw_output["pooler_output"]    # Shape is [batch_size, 1024]

        context_output = self.roberta_model(context_input_ids, context_attention_mask, return_dict=True)
        context_pooler = context_output["pooler_output"]   # Shape is [batch_size, 1024]

        pooler = torch.cat((input_pooler, context_pooler), dim=1)
        output = self.classifier(pooler)                    # Shape is [batch_size, 1]
        return output
    

# English text+audio model + context
class rob_d2v_cc_context(nn.Module):            
    def __init__(self, config):        
        super().__init__()
        self.roberta_model = RobertaModel.from_pretrained('./models/roberta-base', local_files_only=True)
        self.data2vec_model = Data2VecAudioModel.from_pretrained('./models/facebook_data2vec-audio-base', local_files_only=True, attn_implementation="eager")
        #self.hubert_model = HubertModel.from_pretrained('./models/TencentGameMate/chinese-hubert-base',local_files_only=True)

        self.T_output_layers = nn.Sequential(
            nn.Dropout(config.dropout),
            # nn.Linear(768, 1),
            nn.Linear(768, 384),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(384, 1),
        

            

            #nn.ReLU()
           )           
        self.A_output_layers = nn.Sequential(
            nn.Dropout(config.dropout),
            #nn.Linear(1536, 1),

            nn.Linear(1536, 768),
            nn.ReLU(),
            nn.Dropout(config.dropout),

            nn.Linear(768, 1)

            

            #nn.ReLU()
          )
        self.fused_output_layers = nn.Sequential(
            nn.Dropout(config.dropout),
            nn.Linear(3072, 1024*2),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1),

            #nn.ReLU()
        )
        
        
    def forward(self, text_inputs, text_mask, text_context_inputs, text_context_mask, audio_inputs, audio_mask, audio_context_inputs, audio_context_mask):
        # text feature extraction
        raw_output = self.roberta_model(text_inputs, text_mask, return_dict=True)        
        input_pooler = raw_output["pooler_output"]    # Shape is [batch_size, 1024]

        # text context feature extraction
        raw_output_context = self.roberta_model(text_context_inputs, text_context_mask, return_dict=True)
        context_pooler = raw_output_context["pooler_output"]    # Shape is [batch_size, 1024]

        # audio feature extraction
        audio_out = self.data2vec_model(audio_inputs, audio_mask, output_attentions=True)
        A_hidden_states = audio_out.last_hidden_state
        """
        audio_out = self.hubert_model(audio_inputs, audio_mask, output_attentions=True)
        A_hidden_states = audio_out.last_hidden_state
        """
        ## average over unmasked audio tokens
        A_features = []
        audio_mask_idx_new = []
        for batch in range(A_hidden_states.shape[0]):
            layer = 0
            padding_idx = A_hidden_states.shape[1]  # 默认使用全部序列长度
            while layer<12:
                try:
                    padding_idx = sum(audio_out.attentions[layer][batch][0][0]!=0)
                    audio_mask_idx_new.append(padding_idx)
                    break
                except:
                    layer += 1
            # 如果所有层都失败，使用默认值
            if layer >= 12:
                audio_mask_idx_new.append(padding_idx)
            truncated_feature = torch.mean(A_hidden_states[batch][:padding_idx],0) #Shape is [768]
            A_features.append(truncated_feature)
        A_features = torch.stack(A_features,0).to(device)   # Shape is [batch_size, 768]
        
        # audio context feature extraction
        
        audio_context_out = self.data2vec_model(audio_context_inputs, audio_context_mask, output_attentions=True)
        A_context_hidden_states = audio_context_out.last_hidden_state
        """
        audio_context_out = self.hubert_model(audio_context_inputs, audio_context_mask, output_attentions=True)
        A_context_hidden_states = audio_context_out.last_hidden_state
        """
        ## average over unmasked audio tokens
        A_context_features = []
        audio_context_mask_idx_new = []
        for batch in range(A_context_hidden_states.shape[0]):
            layer = 0
            padding_idx = A_context_hidden_states.shape[1]  # 默认使用全部序列长度
            while layer<12:
                try:
                    padding_idx = sum(audio_context_out.attentions[layer][batch][0][0]!=0)
                    audio_context_mask_idx_new.append(padding_idx)
                    break
                except:
                    layer += 1
            # 如果所有层都失败，使用默认值
            if layer >= 12:
                audio_context_mask_idx_new.append(padding_idx)
            truncated_feature = torch.mean(A_context_hidden_states[batch][:padding_idx],0) #Shape is [768]
            A_context_features.append(truncated_feature)
        A_context_features = torch.stack(A_context_features,0).to(device)   # Shape is [batch_size, 768]

        T_features = torch.cat((input_pooler, context_pooler), dim=1)    # Shape is [batch_size, 1024*2]
        A_features = torch.cat((A_features, A_context_features), dim=1)  # Shape is [batch_size, 768*2]
        T_output = self.T_output_layers(T_features)                    # Shape is [batch_size, 1]
        A_output = self.A_output_layers(A_features)                    # Shape is [batch_size, 1]
        
        fused_features = torch.cat((T_features, A_features), dim=1)    # Shape is [batch_size, 1024*2+768*2]
        fused_output = self.fused_output_layers(fused_features)        # Shape is [batch_size, 1]

        return {
                'T': T_output, 
                'A': A_output, 
                'M': fused_output
        }

        # fusing them into one alpha by using DS_combin
        fused_result_alpha = self.DS_Combin_two(fused_alpha, self.DS_Combin_two(T_alpha, A_alpha))
        

        # return {
        #     'T': T_alpha - 100,
        #     'A': A_alpha - 100,
        #     'P': fused_alpha - 100,
        #     'M': fused_result_alpha - 100
        # }

    def DS_Combin_two(self, alpha1, alpha2):
        # Calculate the merger of two DS evidences
        alpha = dict()
        alpha[0], alpha[1] = alpha1, alpha2
        b, S, E, u = dict(), dict(), dict(), dict()
        for v in range(2):
            S[v] = torch.sum(alpha[v], dim=1, keepdim=True)
            E[v] = alpha[v] - 1
            b[v] = E[v] / (S[v].expand(E[v].shape))
            u[v] = 1 / S[v]

        # b^0 @ b^(0+1)
        bb = torch.bmm(b[0].view(-1, 1, 1), b[1].view(-1, 1, 1))
        # b^0 * u^1
        uv1_expand = u[1].expand(b[0].shape)
        bu = torch.mul(b[0], uv1_expand)
        # b^1 * u^0
        uv_expand = u[0].expand(b[0].shape)
        ub = torch.mul(b[1], uv_expand)
        # calculate K
        bb_sum = torch.sum(bb, dim=(1, 2), out=None)
        bb_diag = torch.diagonal(bb, dim1=-2, dim2=-1).sum(-1)
        # bb_diag1 = torch.diag(torch.mm(b[v], torch.transpose(b[v+1], 0, 1)))
        K = bb_sum - bb_diag

        # calculate b^a
        b_a = (torch.mul(b[0], b[1]) + bu + ub) / ((1 - K).view(-1, 1).expand(b[0].shape))
        # calculate u^a
        u_a = torch.mul(u[0], u[1]) / ((1 - K).view(-1, 1).expand(u[0].shape))
        # test = torch.sum(b_a, dim = 1, keepdim = True) + u_a #Verify programming errors

        # calculate new S
        S_a = 1 / u_a
        # calculate new e_k
        e_a = torch.mul(b_a, S_a.expand(b_a.shape))
        alpha_a = e_a + 1
        return alpha_a


# English text+audio model + context + cme
class rob_d2v_cme_context(nn.Module):            
    def __init__(self, config):        
        super().__init__()
        self.roberta_model = RobertaModel.from_pretrained('./models/roberta-large', local_files_only=True)
        self.data2vec_model = Data2VecAudioModel.from_pretrained('./models/facebook_data2vec-audio-large-960h', local_files_only=True, attn_implementation="eager")
        #self.hubert_model = HubertModel.from_pretrained('./models/TencentGameMate/chinese-hubert-base',local_files_only=True)
        self.n_classes = config.n_classes

        self.T_output_layers = nn.Sequential(
            nn.Dropout(config.dropout),
            #nn.Linear(2048, 1),

            nn.Linear(2048, 768),  # 1024*2 = 2048
            nn.ReLU(),
            nn.Dropout(config.dropout),

            nn.Linear(768, self.n_classes),

            # nn.ReLU()
           )           
        self.A_output_layers = nn.Sequential(
            nn.Dropout(config.dropout),
            #nn.Linear(2048, 1),

            nn.Linear(2048, 768),  # 1024*2 = 2048
            nn.ReLU(),
            nn.Dropout(config.dropout),

            nn.Linear(768, self.n_classes),

            # nn.ReLU()
          )
        # self.fused_output_layers = nn.Sequential(
        #     nn.Dropout(config.dropout),
        #     nn.Linear(768*4, 768),
        #     nn.ReLU(),
        #     nn.Linear(768, 1),

        #     #nn.ReLU()
        # )
        
        # cls embedding layers
        self.text_cls_emb = nn.Embedding(num_embeddings=1, embedding_dim=1024)  # RoBERTa-large 是 1024 维
        self.audio_cls_emb = nn.Embedding(num_embeddings=1, embedding_dim=1024)  # Data2Vec-large 是 1024 维

        # CME layers
        Bert_config = BertConfig(num_hidden_layers=config.num_hidden_layers, hidden_size=1024, intermediate_size=4096, num_attention_heads=16)
        self.CME_layers = nn.ModuleList(
            [CMELayer(Bert_config) for _ in range(Bert_config.num_hidden_layers)]
        )
        
        
    def prepend_cls(self, inputs, masks, layer_name):
        if layer_name == 'text':
            embedding_layer = self.text_cls_emb
        elif layer_name == 'audio':
            embedding_layer = self.audio_cls_emb
        index = torch.LongTensor([0]).to(device=inputs.device)
        cls_emb = embedding_layer(index)
        cls_emb = cls_emb.expand(inputs.size(0), 1, inputs.size(2))
        outputs = torch.cat((cls_emb, inputs), dim=1)
        
        cls_mask = torch.ones(inputs.size(0), 1).to(device=inputs.device)
        masks = torch.cat((cls_mask, masks), dim=1)
        return outputs, masks
    
    def forward(self, text_inputs, text_mask, text_context_inputs, text_context_mask, audio_inputs, audio_mask, audio_context_inputs, audio_context_mask):
        # text feature extraction
        raw_output = self.roberta_model(text_inputs, text_mask, return_dict=True)
        T_hidden_states = raw_output.last_hidden_state
        input_pooler = raw_output["pooler_output"]    # Shape is [batch_size, 1024]

        # text context feature extraction
        raw_output_context = self.roberta_model(text_context_inputs, text_context_mask, return_dict=True)
        T_context_hidden_states = raw_output_context.last_hidden_state
        context_pooler = raw_output_context["pooler_output"]    # Shape is [batch_size, 1024]

        # audio feature extraction
        
        audio_out = self.data2vec_model(audio_inputs, audio_mask, output_attentions=True)
        A_hidden_states = audio_out.last_hidden_state
        """
        audio_out = self.hubert_model(audio_inputs, audio_mask, output_attentions=True)
        A_hidden_states = audio_out.last_hidden_state
        """
        ## average over unmasked audio tokens
        A_features = []
        audio_mask_idx_new = []
        for batch in range(A_hidden_states.shape[0]):
            layer = 0
            padding_idx = A_hidden_states.shape[1]  # 默认使用全部序列长度
            while layer<24:  # data2vec-audio-large 有 24 层
                try:
                    padding_idx = sum(audio_out.attentions[layer][batch][0][0]!=0)
                    audio_mask_idx_new.append(padding_idx)
                    break
                except:
                    layer += 1
            # 如果所有层都失败，使用默认值
            if layer >= 24:
                audio_mask_idx_new.append(padding_idx)
            truncated_feature = torch.mean(A_hidden_states[batch][:padding_idx],0) #Shape is [1024]
            A_features.append(truncated_feature)
        A_features = torch.stack(A_features,0).to(device)   # Shape is [batch_size, 1024]
        audio_mask_new = torch.zeros(A_hidden_states.shape[0], A_hidden_states.shape[1]).to(device)
        for batch in range(audio_mask_new.shape[0]):
            audio_mask_new[batch][:audio_mask_idx_new[batch]] = 1

        # audio context feature extraction
        
        audio_context_out = self.data2vec_model(audio_context_inputs, audio_context_mask, output_attentions=True)
        A_context_hidden_states = audio_context_out.last_hidden_state
        """
        audio_context_out = self.hubert_model(audio_context_inputs, audio_context_mask, output_attentions=True)
        A_context_hidden_states = audio_context_out.last_hidden_state
        """
        ## average over unmasked audio tokens
        A_context_features = []
        audio_context_mask_idx_new = []
        for batch in range(A_context_hidden_states.shape[0]):
            layer = 0
            padding_idx = A_context_hidden_states.shape[1]  # 默认使用全部序列长度
            while layer<24:  # data2vec-audio-large 有 24 层
                try:
                    padding_idx = sum(audio_context_out.attentions[layer][batch][0][0]!=0)
                    audio_context_mask_idx_new.append(padding_idx)
                    break
                except:
                    layer += 1
            # 如果所有层都失败，使用默认值
            if layer >= 24:
                audio_context_mask_idx_new.append(padding_idx)
            truncated_feature = torch.mean(A_context_hidden_states[batch][:padding_idx],0) #Shape is [1024]
            A_context_features.append(truncated_feature)
        A_context_features = torch.stack(A_context_features,0).to(device)   # Shape is [batch_size, 1024]
        audio_context_mask_new = torch.zeros(A_context_hidden_states.shape[0], A_context_hidden_states.shape[1]).to(device)
        for batch in range(audio_context_mask_new.shape[0]):
            audio_context_mask_new[batch][:audio_context_mask_idx_new[batch]] = 1

        T_features = torch.cat((input_pooler, context_pooler), dim=1)    # Shape is [batch_size, 1024*2]
        A_features = torch.cat((A_features, A_context_features), dim=1)  # Shape is [batch_size, 1024*2]
        T_output = self.T_output_layers(T_features)                    # Shape is [batch_size, 1]
        A_output = self.A_output_layers(A_features)                    # Shape is [batch_size, 1]
        
        # # CME layers
        # text_inputs, text_attn_mask = self.prepend_cls(T_hidden_states, text_mask, 'text') # add cls token
        # audio_inputs, audio_attn_mask = self.prepend_cls(A_hidden_states, audio_mask_new, 'audio') # add cls token

        # text_context_inputs, text_context_attn_mask = self.prepend_cls(T_context_hidden_states, text_context_mask, 'text') # add cls token
        # audio_context_inputs, audio_context_attn_mask = self.prepend_cls(A_context_hidden_states, audio_context_mask_new, 'audio') # add cls token
        
        # for layer_module in self.CME_layers:
        #     text_inputs, audio_inputs = layer_module(text_inputs, text_attn_mask,
        #                                         audio_inputs, audio_attn_mask)
        
        # for layer_module in self.CME_layers:
        #     text_context_inputs, audio_context_inputs = layer_module(text_context_inputs, text_context_attn_mask,
        #                                         audio_context_inputs, audio_context_attn_mask)


        # # fused features
        # fused_hidden_states = torch.cat((text_inputs[:,0,:], text_context_inputs[:,0,:], audio_inputs[:,0,:],  audio_context_inputs[:,0,:]), dim=1) # Shape is [batch_size, 1024*4]

        # # last linear output layer
        # fused_output = self.fused_output_layers(fused_hidden_states) # Shape is [batch_size, 1]

        # max_evidence = 100.0             # 你可以根据实际调整
        
        
        # calculate alphas for all modules
        T_alpha = F.softplus(T_output) + 1
        A_alpha = F.softplus(A_output) + 1
        # # fused_alpha = fused_output + 1
        # evidence = torch.clamp(T_alpha, max=max_evidence)
        # evidence = torch.clamp(A_alpha, max=max_evidence)
        # fusing them into one alpha by using DS_combin
        fused_result_alpha = self.DS_Combin_two(T_alpha, A_alpha)

        # 检查合法性
        check_alpha_valid(T_alpha)
        check_alpha_valid(A_alpha)
        check_alpha_valid(fused_result_alpha)

        return {
            'T': T_alpha,
            'A': A_alpha,
            'M': fused_result_alpha
        }

    def DS_Combin_two(self, alpha1, alpha2):
        # Calculate the merger of two DS evidences
        alpha = dict()
        alpha[0], alpha[1] = alpha1, alpha2
        b, S, E, u = dict(), dict(), dict(), dict()
        for v in range(2):
            S[v] = torch.sum(alpha[v], dim=1, keepdim=True)
            E[v] = alpha[v] - 1
            b[v] = E[v] / (S[v].expand(E[v].shape))
            u[v] = self.n_classes / S[v]

        # b^0 @ b^(0+1)
        bb = torch.bmm(b[0].view(-1, self.n_classes, 1), b[1].view(-1, 1, self.n_classes))
        # b^0 * u^1
        uv1_expand = u[1].expand(b[0].shape)
        bu = torch.mul(b[0], uv1_expand)
        # b^1 * u^0
        uv_expand = u[0].expand(b[0].shape)
        ub = torch.mul(b[1], uv_expand)
        # calculate K
        bb_sum = torch.sum(bb, dim=(1, 2), out=None)
        bb_diag = torch.diagonal(bb, dim1=-2, dim2=-1).sum(-1)
        # bb_diag1 = torch.diag(torch.mm(b[v], torch.transpose(b[v+1], 0, 1)))
        K = bb_sum - bb_diag

        # calculate b^a
        b_a = (torch.mul(b[0], b[1]) + bu + ub) / ((1 - K).view(-1, 1).expand(b[0].shape))
        # calculate u^a
        u_a = torch.mul(u[0], u[1]) / ((1 - K).view(-1, 1).expand(u[0].shape))
        # test = torch.sum(b_a, dim = 1, keepdim = True) + u_a #Verify programming errors

        # calculate new S
        S_a = self.n_classes / u_a
        # calculate new e_k
        e_a = torch.mul(b_a, S_a.expand(b_a.shape))
        alpha_a = e_a + 1
        return alpha_a

def check_alpha_valid(alpha, name="alpha"):
    """
    检查 α 是否有效:
    1. 必须 >= 1
    2. 不包含 NaN
    3. 不包含 Inf
    """
    assert torch.all(alpha >= 1), f"{name} 含有小于 1 的值: {alpha.min().item()}"
    assert not torch.isnan(alpha).any(), f"{name} 含有 NaN"
    assert not torch.isinf(alpha).any(), f"{name} 含有 Inf"
# def shift_evidence(evidence, min_val=1.0 + 1e-5):
#     """
#     对整个 evidence 数组做平移，使最小值 >= min_val。
    
#     Args:
#         evidence: torch.Tensor, [B, C] 或任意形状
#         min_val: float, 最小值下界（默认为 1）
    
#     Returns:
#         shifted_evidence: torch.Tensor, 平移后的 evidence
#     """
#     # 计算当前最小值
#     cur_min = torch.min(evidence)
    
#     # 需要平移的量
#     shift = min_val - cur_min
    
#     # 平移
#     shifted_evidence = evidence + shift
    
#     return shifted_evidence