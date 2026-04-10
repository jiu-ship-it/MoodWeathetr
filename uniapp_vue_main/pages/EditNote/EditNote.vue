<template>
	<view class="flex-col page">

		<view class="flex-col justify-start items-start text-wrapper"><text class="text">MoodWeather</text></view>

		<view class="flex-col section mt-25">

			<view class="flex-col">
				<text class="self-start font text_2">标题</text>
				<textarea v-model="title" class="flex-col justify-start items-start self-stretch text-wrapper_2" placeholder="请输入标题">
          <!-- <text class="font_2 text_3">请输入标题</text> -->
        </textarea>
				<text class="self-start font text_4">内容</text>
				<textarea v-model="content" maxlength="1000" class="flex-col justify-start items-start self-stretch text-wrapper_3"
					warp="soft" placeholder="请输入内容">
          <!-- <text class="font_2 text_5">请输入内容</text> -->
        </textarea>

				<text class="self-start font text_6">选择当前情绪(必) 当前：{{ ChooseEmoPop }}</text>
				<view>
					<image class="image" :class="{ 'image-selected': ChooseEmoPop === 1 }" src="/static/image/smileICON.png"
						@click="ChooseEmoPop = 1" />
					<image class="image" :class="{ 'image-selected': ChooseEmoPop === 2 }" src="/static/image/little.png"
						@click="ChooseEmoPop = 2" />
					<image class="image" :class="{ 'image-selected': ChooseEmoPop === 3 }" src="/static/image/Unhappy.png"
						@click="ChooseEmoPop = 3" />
				</view>
			</view>

			<view class="flex-col mt-27">
				<view class="flex-col group">
					<text class="self-start font text_7">您可以上传录音（点击录音）</text>
					<view class="flex-row justify-between items-center self-stretch group_2 mt-9">
						<image class="image_2" :class="{ recording: tips_visible === 'visible' }" src="/static/image/Speak.png"
							@click="SaveRecord" />
						<view class="record-dot" :style="{visibility:tips_visible}"></view>
						<text :style="{visibility:tips_visible}">正在录音（{{ formatRecordTime() }}）</text>
						<image class="image_3" src="/static/image/play.png" :style="{visibility:CanPlay_visible}"
							@click="playVoice" />
					</view>
					<text v-if="hasSavedAudio" class="self-start font record-info">该条历史录音时长：{{ recordedSeconds > 0 ? formatDuration(recordedSeconds) : '未统计' }}</text>
				</view>
				<view class="flex-row group_3">
					<view class="flex-col justify-start items-center text-wrapper_4" @click="saveNote(true)">
						<text class="font text_8">保存并退出</text>
					</view>
					<view class="flex-col justify-start items-center text-wrapper_5 ml-15" @click="saveNote(false)">
						<text class="font text_9">保存</text>
					</view>
				</view>
			</view>

		</view>
	</view>
</template>

<script>
	import { BASE_URL } from '@/common/config.js';

	const recorderManager = uni.getRecorderManager(); //设置录音
	const innerAudioContext = uni.createInnerAudioContext(); //设置播放

	export default {
		components: {},
		props: {},
		data() {
			return {
				title: '',
				content: '',
				noteId: null,
				ChooseEmoPop: 1,
				tips_visible: "hidden",
				CanPlay_visible: "hidden",
				voicePath: '',
				recordedSeconds: 0,
				hasSavedAudio: false,
				isRecordAuth: false,
				isplay: false,
				h5Recorder: null,
				h5Stream: null,
				h5Chunks: [],
				h5AudioFile: null,
				recordSeconds: 0,
				recordTimer: null
			};
		},
		onLoad(options) {
			let self = this;
			innerAudioContext.onEnded(() => {
				this.isplay = false;
			});
			innerAudioContext.onError(() => {
				this.isplay = false;
				uni.showToast({ title: '录音播放失败', icon: 'none' });
			});
			if (options && options.id) {
				this.noteId = options.id;
				this.fetchNoteDetail();
			}
			recorderManager.onStop(function(res) {
				self.persistAppVoiceFile(res.tempFilePath);
				self.recordedSeconds = self.recordSeconds;
				self.hasSavedAudio = true;
				self.CanPlay_visible = "visible";
				self.tips_visible = "hidden";
				self.stopRecordTimer();
			});
		},
		onUnload() {
			this.stopRecordTimer();
			if (this.h5Stream) {
				this.h5Stream.getTracks().forEach((track) => track.stop());
				this.h5Stream = null;
			}
		},
		methods: {
			persistAppVoiceFile(tempFilePath) {
				if (!tempFilePath) {
					this.voicePath = '';
					this.hasSavedAudio = false;
					return;
				}
				uni.saveFile({
					tempFilePath,
					success: (res) => {
						this.voicePath = res.savedFilePath || tempFilePath;
						this.hasSavedAudio = true;
					},
					fail: () => {
						this.voicePath = tempFilePath;
						this.hasSavedAudio = true;
					}
				});
			},
			startRecordTimer() {
				this.stopRecordTimer();
				this.recordSeconds = 0;
				this.recordTimer = setInterval(() => {
					this.recordSeconds += 1;
				}, 1000);
			},
			stopRecordTimer() {
				if (this.recordTimer) {
					clearInterval(this.recordTimer);
					this.recordTimer = null;
				}
			},
			formatRecordTime() {
				const minutes = Math.floor(this.recordSeconds / 60);
				const seconds = this.recordSeconds % 60;
				const mm = minutes < 10 ? `0${minutes}` : `${minutes}`;
				const ss = seconds < 10 ? `0${seconds}` : `${seconds}`;
				return `${mm}:${ss}`;
			},
			formatDuration(totalSeconds) {
				const value = Number(totalSeconds) || 0;
				const minutes = Math.floor(value / 60);
				const seconds = value % 60;
				const mm = minutes < 10 ? `0${minutes}` : `${minutes}`;
				const ss = seconds < 10 ? `0${seconds}` : `${seconds}`;
				return `${mm}:${ss}`;
			},
			goBackAfterSave() {
				const pages = getCurrentPages ? getCurrentPages() : [];
				if (pages && pages.length > 1) {
					uni.navigateBack({ delta: 1 });
					return;
				}
				uni.reLaunch({ url: '/pages/MainNoteSet/MainNoteSet' });
			},
			saveNote(exitAfterSave) {
				if (!this.title || !this.content) {
					uni.showToast({
						title: '请填写标题和内容',
						icon: 'none'
					});
					return;
				}
				if (!this.ChooseEmoPop) {
					uni.showToast({
						title: '请选择情绪',
						icon: 'none'
					});
					return;
				}

				uni.showLoading({ title: '保存中...' });

				const token = uni.getStorageSync('token');
				const apiBase = `${BASE_URL}/api`;
				const isUpdate = !!this.noteId;
				const targetUrl = isUpdate ? `${apiBase}/notes/${this.noteId}` : `${apiBase}/notes`;
				const captureNoteId = (payload) => {
					if (!isUpdate && payload && payload.note_id) {
						this.noteId = payload.note_id;
					}
				};

				if (this.voicePath) {
					// #ifdef H5
					if (this.h5AudioFile) {
						uni.uploadFile({
							url: targetUrl,
							method: isUpdate ? 'PUT' : 'POST',
							files: [{ name: 'audio', file: this.h5AudioFile }],
							header: { 'Authorization': 'Bearer ' + token },
							formData: {
								title: this.title,
								content: this.content,
								emotion: this.ChooseEmoPop,
								audio_duration: this.recordedSeconds || 0
							},
							success: (res) => {
								uni.hideLoading();
								if (res.statusCode === 201 || res.statusCode === 200) {
									let payload = null;
									if (typeof res.data === 'string') {
										try {
											payload = JSON.parse(res.data);
										} catch (e) {
											payload = null;
										}
									} else {
										payload = res.data;
									}
									captureNoteId(payload);
									uni.showToast({ title: '保存成功', icon: 'success' });
									if (exitAfterSave) this.goBackAfterSave();
								} else {
									uni.showToast({ title: '保存失败', icon: 'none' });
								}
							},
							fail: () => {
								uni.hideLoading();
								uni.showToast({ title: '网络错误', icon: 'none' });
							}
						});
						return;
					}
					// #endif

					uni.uploadFile({
						url: targetUrl,
						method: isUpdate ? 'PUT' : 'POST',
						filePath: this.voicePath,
						name: 'audio',
						header: { 'Authorization': 'Bearer ' + token },
						formData: {
							title: this.title,
							content: this.content,
							emotion: this.ChooseEmoPop,
							audio_duration: this.recordedSeconds || 0
						},
						success: (res) => {
							uni.hideLoading();
							if (res.statusCode === 201 || res.statusCode === 200) {
								let payload = null;
								if (typeof res.data === 'string') {
									try {
										payload = JSON.parse(res.data);
									} catch (e) {
										payload = null;
									}
								} else {
									payload = res.data;
								}
								captureNoteId(payload);
								uni.showToast({ title: '保存成功', icon: 'success' });
								if (exitAfterSave) this.goBackAfterSave();
							} else {
								uni.showToast({ title: '保存失败', icon: 'none' });
							}
						},
						fail: () => {
							uni.hideLoading();
							uni.showToast({ title: '网络错误', icon: 'none' });
						}
					});
				} else {
					uni.request({
						url: targetUrl,
						method: isUpdate ? 'PUT' : 'POST',
						header: {
							'Authorization': 'Bearer ' + token,
							'Content-Type': 'application/json'
						},
						data: {
							title: this.title,
							content: this.content,
							emotion: this.ChooseEmoPop,
							audio_duration: this.recordedSeconds || 0
						},
						success: (res) => {
							uni.hideLoading();
							if (res.statusCode === 201 || res.statusCode === 200) {
								captureNoteId(res.data);
								uni.showToast({ title: '保存成功', icon: 'success' });
								if (exitAfterSave) this.goBackAfterSave();
							} else {
								uni.showToast({ title: '保存失败', icon: 'none' });
							}
						},
						fail: () => {
							uni.hideLoading();
							uni.showToast({ title: '网络错误', icon: 'none' });
						}
					});
				}
			},
			fetchNoteDetail() {
				const token = uni.getStorageSync('token');
				const apiBase = `${BASE_URL}/api`;
				uni.request({
					url: `${apiBase}/notes/${this.noteId}`,
					header: { 'Authorization': 'Bearer ' + token },
					success: (res) => {
						if (res.statusCode === 200 && res.data) {
							this.title = res.data.title || '';
							this.content = res.data.content || '';
							this.ChooseEmoPop = Number(res.data.emotion) || 1;
							this.recordedSeconds = Number(res.data.audio_duration) || 0;
							if (res.data.audio_path) {
								this.hasSavedAudio = true;
								this.CanPlay_visible = 'visible';
								this.loadSavedAudio(token);
							} else {
								this.hasSavedAudio = false;
								this.voicePath = '';
								this.CanPlay_visible = 'hidden';
							}
						}
					}
				});
			},
			loadSavedAudio(token) {
				const apiBase = `${BASE_URL}/api`;
				return new Promise((resolve, reject) => {
					uni.downloadFile({
						url: `${apiBase}/notes/${this.noteId}/audio`,
						header: { 'Authorization': 'Bearer ' + token },
						success: (res) => {
							if (res.statusCode === 200 && res.tempFilePath) {
								this.voicePath = res.tempFilePath;
								this.hasSavedAudio = true;
								this.CanPlay_visible = 'visible';
								resolve(res.tempFilePath);
								return;
							}
							this.voicePath = '';
							this.hasSavedAudio = false;
							this.CanPlay_visible = 'hidden';
							reject(new Error('download failed'));
						},
						fail: () => {
							this.voicePath = '';
							this.hasSavedAudio = false;
							this.CanPlay_visible = 'hidden';
							reject(new Error('download failed'));
						}
					});
				});
			},
			async SaveRecord() { //异步操作，防止上方函数未执行，直接执行下一步操作
				// #ifdef H5
				if (this.tips_visible === "hidden") {
					this.startH5Record();
				} else {
					this.stopH5Record();
				}
				return;
				// #endif

				// #ifdef MP-WEIXIN
				if (this.tips_visible == "hidden") {
					uni.authorize({
						scope: 'scope.record',
						success: () => {
							this.isRecordAuth = true;
							this.tips_visible = "visible";
							this.recordedSeconds = 0;
							this.hasSavedAudio = false;
							this.CanPlay_visible = "hidden";
							this.startRecordTimer();
							innerAudioContext.stop();
							recorderManager.start({
								duration: 600000,
								sampleRate: 16000,
								numberOfChannels: 1,
								format: 'wav'
							});
						},
						fail: () => {
							this.isRecordAuth = false;
							uni.showModal({
								title: '需要录音权限',
								content: '请在设置中开启麦克风权限后重试',
								confirmText: '去设置',
								success: (res) => {
									if (res.confirm) {
										uni.openSetting({});
									}
								}
							});
						}
					});
				} else {
					this.tips_visible = "hidden";
					this.CanPlay_visible = "visible";
					this.stopRecordTimer();
					recorderManager.stop();
				}
				return;
				// #endif

				// #ifdef APP-PLUS
				await this.applyRecordAuth();
				if (this.isRecordAuth == false) {
					uni.showToast({
						title: "录音权限未打开",
						icon: 'none',
						duration: 2000
					})
				}
				if (this.tips_visible == "hidden" && this.isRecordAuth) {
					this.tips_visible = "visible";
					this.recordedSeconds = 0;
					this.hasSavedAudio = false;
					this.CanPlay_visible = "hidden";
					this.startRecordTimer();
					uni.showToast({
						title: "录音权限已打开",
						icon: 'none',
						duration: 2000
					})
					innerAudioContext.stop();
					recorderManager.start({
						duration: 600000,
						format: 'wav', // 录音格式     
					});
				} else if (this.tips_visible == "visible" && this.isRecordAuth) {
					uni.showToast({
						title: "录音结束",
						icon: 'none',
						duration: 2000
					})
					this.tips_visible = "hidden";
					this.CanPlay_visible = "visible";
					this.stopRecordTimer();
					recorderManager.stop();
				}
				// #endif
			},

			startH5Record() {
				if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') {
					uni.showToast({
						title: "当前浏览器不支持录音",
						icon: "none",
						duration: 2000
					});
					return;
				}

				this.h5Chunks = [];
				this.h5AudioFile = null;
				this.recordedSeconds = 0;
				this.hasSavedAudio = false;
				this.tips_visible = "visible";
				this.CanPlay_visible = "hidden";
				this.startRecordTimer();
				uni.showToast({
					title: "开始录音",
					icon: "none",
					duration: 1500
				});

				navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
					this.h5Stream = stream;
					const preferredTypes = [
						'audio/ogg;codecs=opus',
						'audio/webm;codecs=opus',
						'audio/webm'
					];
					let selectedType = '';
					preferredTypes.some((type) => {
						if (MediaRecorder.isTypeSupported(type)) {
							selectedType = type;
							return true;
						}
						return false;
					});

					const recorder = selectedType ? new MediaRecorder(stream, { mimeType: selectedType }) : new MediaRecorder(stream);
					this.h5Recorder = recorder;
					this.isRecordAuth = true;

					recorder.ondataavailable = (event) => {
						if (event.data && event.data.size > 0) {
							this.h5Chunks.push(event.data);
						}
					};
					recorder.onstop = () => {
						const mimeType = recorder.mimeType || 'audio/webm';
						const blob = new Blob(this.h5Chunks, { type: mimeType });
						const ext = mimeType.includes('ogg') ? 'ogg' : 'webm';
						const filename = `record_${Date.now()}.${ext}`;
						this.h5AudioFile = new File([blob], filename, { type: mimeType });
						if (this.voicePath) {
							URL.revokeObjectURL(this.voicePath);
						}
						this.voicePath = URL.createObjectURL(blob);
						this.recordedSeconds = this.recordSeconds;
						this.hasSavedAudio = true;
						this.CanPlay_visible = "visible";
					};

					recorder.start();
				}).catch(() => {
					this.tips_visible = "hidden";
					this.stopRecordTimer();
					this.isRecordAuth = false;
					uni.showToast({
						title: "麦克风权限被拒绝",
						icon: "none",
						duration: 2000
					});
				});
			},

			stopH5Record() {
				this.recordedSeconds = this.recordSeconds;
				this.tips_visible = "hidden";
				this.stopRecordTimer();
				uni.showToast({
					title: "录音结束",
					icon: "none",
					duration: 1500
				});
				if (this.h5Recorder && this.h5Recorder.state !== 'inactive') {
					this.h5Recorder.stop();
				}
				if (this.h5Stream) {
					this.h5Stream.getTracks().forEach((track) => track.stop());
					this.h5Stream = null;
				}
			},

			async applyRecordAuth() {//判断是否打开必要权限
				try {
					if (typeof plus === 'undefined' || !plus.android) {
						uni.showToast({
							title: "当前平台不支持录音权限获取",
							icon: "none",
							duration: 2000
						});
						this.isRecordAuth = false;
						return;
					}

					const RECORD_PERM = "android.permission.RECORD_AUDIO";
					// 1. 定义安卓原生Activity（修复未定义问题）
					const mainActivity = plus.android.runtimeMainActivity();
					// 2. 原生常量（数值：0=授权，-1=未授权）
					const PERM_GRANTED = mainActivity.PERMISSION_GRANTED;
					const PERM_DENIED = mainActivity.PERMISSION_DENIED;

					// ===== 修复：区分5+ API和原生API的判断逻辑 =====
					// 方式1：用安卓原生API（推荐，数值判断更精准）
					const authState = mainActivity.checkSelfPermission(RECORD_PERM);
					// 方式2：若坚持用5+ API，需判断字符串（二选一）
					// const authState = plus.android.checkPermission(RECORD_PERM);

					// 已授权（适配原生API的数值判断）
					if (authState === PERM_GRANTED || authState === 0) {
						this.isRecordAuth = true;
						uni.showToast({
							title: "录音权限已开启",
							icon: "none"
						});
						return;
					}

					// 未授权：动态申请权限
					const isGranted = await new Promise(resolve => {
						plus.android.requestPermissions([RECORD_PERM], (res) => {
							resolve(res[0]?.granted); // 返回布尔值：true=授权，false=拒绝
						});
					});

					// 处理申请结果（正常流程：授权/拒绝）
					if (isGranted) {
						this.isRecordAuth = true;
						uni.showToast({
							title: "录音权限已授权",
							icon: "none"
						});
					} else {
						// 拒绝授权：引导去设置（修复逻辑位置）
						uni.showModal({
							title: "需要麦克风权限",
							content: "请前往设置开启录音权限",
							confirmText: "去设置",
							cancelText: "取消",
							success: (res) => {
								if (res.confirm) {
									// 原生跳转设置页（必成功）
									const Intent = plus.android.importClass("android.content.Intent");
									const Settings = plus.android.importClass("android.provider.Settings");
									const Uri = plus.android.importClass("android.net.Uri");
									const intent = new Intent(Settings
									.ACTION_APPLICATION_DETAILS_SETTINGS);
									intent.setData(Uri.parse("package:" + mainActivity.getPackageName()));
									mainActivity.startActivity(intent);
									this.isRecordAuth = true;
								}
							}
						});
					}
				} catch (err) {
					// 代码报错时的兜底（如API调用失败）
					console.error("权限检测/申请失败：", err);
					uni.showModal({
						title: "权限异常",
						content: "请手动前往设置开启录音权限",
						confirmText: "去设置",
						success: (res) => {
							if (res.confirm) {
								const mainActivity = plus.android.runtimeMainActivity();
								const Intent = plus.android.importClass("android.content.Intent");
								const Settings = plus.android.importClass("android.provider.Settings");
								const Uri = plus.android.importClass("android.net.Uri");
								const intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
								intent.setData(Uri.parse("package:" + mainActivity.getPackageName()));
								mainActivity.startActivity(intent);
							}
						}
					});
				}
				
			},

			async playVoice() {
				if (!this.voicePath && this.noteId && this.hasSavedAudio) {
					const token = uni.getStorageSync('token');
					try {
						await this.loadSavedAudio(token);
					} catch (e) {
						uni.showToast({ title: '录音加载失败', icon: 'none' });
						return;
					}
				}
				if (this.voicePath && !this.isplay) {
					innerAudioContext.src = this.voicePath;
					innerAudioContext.play();
					this.isplay = true;
				} else if (this.isplay) {
					innerAudioContext.stop();
					this.isplay = false;
				}
			},

		},
	};
</script>

<style scoped lang="css">
	.mt-25 {
		margin-top: 45.51rpx;
	}

	.mt-27 {
		margin-top: 49.15rpx;
	}

	.mt-9 {
		margin-top: 16.38rpx;
	}

	.ml-15 {
		margin-left: 27.31rpx;
	}

	.page {
		padding-bottom: 45.51rpx;
		background-image: linear-gradient(160deg, #f6f7fb 0%, #e8eefc 45%, #dce8ff 100%);
		background-size: 100% 100%;
		background-repeat: no-repeat;
		width: 100%;
		overflow-y: auto;
		overflow-x: hidden;
		height: 100%;
	}

	.text-wrapper {
		padding: 40.05rpx 0;
		background-color: #d9d9d9b3;

	}

	.text {
		margin-left: 25.49rpx;
		color: #000000;
		font-size: 65.53rpx;
		font-family: Inter;
		line-height: 60.62rpx;
	}

	.section {
		height: 80%;
		margin: 0 29.13rpx;
		padding: 50.97rpx 36.41rpx 322.21rpx 43.69rpx;
		opacity: 0.95;
		background-color: #ffffff;
		border-radius: 14.56rpx;
		border-left: solid 1.82rpx #d9d9d9;
		border-right: solid 1.82rpx #d9d9d9;
		border-top: solid 1.82rpx #d9d9d9;
		border-bottom: solid 1.82rpx #d9d9d9;
	}

	.font {
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 26.85rpx;
		color: #1e1e1e;
	}

	.text_2 {
		line-height: 26.76rpx;
	}

	.text-wrapper_2 {
		margin-top: 18.2rpx;
		padding: 21.84rpx 0;
		height: 50rpx;
		background-color: #ffffff;
		border-radius: 14.56rpx;
		overflow: hidden;
		border-left: solid 1.82rpx #d9d9d9;
		border-right: solid 1.82rpx #d9d9d9;
		border-top: solid 1.82rpx #d9d9d9;
		border-bottom: solid 1.82rpx #d9d9d9;
	}

	.font_2 {
		font-size: 29.13rpx;
		font-family: Inter;
		line-height: 26.85rpx;
		color: #b3b3b3;
	}

	.text_3 {
		margin-left: 29.13rpx;
	}

	.text_4 {
		margin-left: 3.64rpx;
		margin-top: 40.05rpx;
	}

	.text-wrapper_3 {
		/* height: 100%;
    margin-top: 18.2rpx;
    padding: 29.13rpx 0 294.9rpx;
    background-color: #ffffff;
    border-radius: 14.56rpx;
    overflow: hidden;
    border-left: solid 1.82rpx #d9d9d9;
    border-right: solid 1.82rpx #d9d9d9;
    border-top: solid 1.82rpx #d9d9d9;
    border-bottom: solid 1.82rpx #d9d9d9; */
		margin-right: 5.83rpx;
		margin-top: 18.2rpx;
		max-width: 100%;
		padding: 121.97rpx 0 9.1rpx;
		padding-top: 20rpx;
		background-color: #ffffff;
		border-radius: 14.56rpx;
		overflow: hidden;
		border: solid 1.82rpx #d9d9d9;
		height: 400rpx;
	}

	.text_5 {
		margin-left: 29.13rpx;
		line-height: 26.94rpx;
	}

	.text_6 {
		margin-top: 32.77rpx;
		line-height: 27rpx;
	}

	.image {
		margin-left: 7.28rpx;
		margin-top: 21.84rpx;
		width: 94.66rpx;
		height: 94.66rpx;
	}

	.image-selected {
		border: 3rpx solid #2c2c2c;
		border-radius: 50%;
		box-shadow: 0 0 10rpx rgba(0, 0, 0, 0.25);
		transform: scale(1.06);
	}

	.group {
		margin-right: 3.64rpx;
		padding-bottom: 16.38rpx;
		overflow: hidden;
	}

	.text_7 {
		line-height: 27.72rpx;
	}

	.group_2 {
		padding: 0 10.92rpx;
	}

	.image_2 {
		width: 69.17rpx;
		height: 103.76rpx;
	}

	.recording {
		filter: drop-shadow(0 0 12rpx rgba(220, 0, 0, 0.65));
		transform: scale(1.08);
		transition: transform 0.2s ease;
		animation: record-pulse 1s ease-in-out infinite;
	}

	.record-dot {
		width: 14rpx;
		height: 14rpx;
		border-radius: 50%;
		background-color: #d40000;
		box-shadow: 0 0 10rpx rgba(212, 0, 0, 0.7);
		animation: record-blink 1s ease-in-out infinite;
	}

	.record-info {
		margin-top: 10rpx;
		color: #4a4a4a;
	}

	.image_3 {
		margin-right: 14.56rpx;
		width: 87.38rpx;
		height: 87.38rpx;
	}

	@keyframes record-pulse {
		0% {
			transform: scale(1.02);
		}
		50% {
			transform: scale(1.12);
		}
		100% {
			transform: scale(1.02);
		}
	}

	@keyframes record-blink {
		0% {
			opacity: 1;
		}
		50% {
			opacity: 0.2;
		}
		100% {
			opacity: 1;
		}
	}

	.group_3 {
		padding-top: 32.77rpx;
	}

	.text-wrapper_4 {
		padding: 21.84rpx 0;
		flex: 1 1 286.71rpx;
		border-radius: 14.56rpx;
		overflow: hidden;
		height: 72.82rpx;
		border-left: solid 1.82rpx #000000;
		border-right: solid 1.82rpx #000000;
		border-top: solid 1.82rpx #000000;
		border-bottom: solid 1.82rpx #000000;
	}

	.text_8 {
		color: #303030;
		line-height: 27.09rpx;
	}

	.text-wrapper_5 {
		margin-right: 3.64rpx;
		padding: 21.84rpx 0;
		flex: 1 1 286.71rpx;
		background-color: #2c2c2c;
		border-radius: 14.56rpx;
		overflow: hidden;
		height: 72.82rpx;
		border-left: solid 1.82rpx #2c2c2c;
		border-right: solid 1.82rpx #2c2c2c;
		border-top: solid 1.82rpx #2c2c2c;
		border-bottom: solid 1.82rpx #2c2c2c;
	}

	.text_9 {
		color: #f5f5f5;
		line-height: 26.8rpx;
	}
</style>