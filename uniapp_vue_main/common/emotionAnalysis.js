export function parseAnalysisPayload(payload) {
  if (!payload) {
    return null;
  }
  if (typeof payload === 'string') {
    try {
      return JSON.parse(payload);
    } catch (e) {
      return null;
    }
  }
  return payload;
}

export function normalizePredictionFromAnalysis(analysis) {
  const probs = analysis && analysis.probabilities && analysis.probabilities.M;
  const classCount = Array.isArray(probs) && probs.length ? probs.length : 3;
  const prediction = Number(analysis && analysis.prediction);

  if (!Number.isNaN(prediction)) {
    if (prediction >= 1 && prediction <= classCount) {
      return prediction;
    }
    if (prediction >= 0 && prediction < classCount) {
      return prediction + 1;
    }
  }

  if (Array.isArray(probs) && probs.length) {
    let maxIdx = 0;
    for (let i = 1; i < probs.length; i += 1) {
      if (Number(probs[i]) > Number(probs[maxIdx])) {
        maxIdx = i;
      }
    }
    return maxIdx + 1;
  }

  return 0;
}

export function isLowAlertFromAnalysis(analysis) {
  return normalizePredictionFromAnalysis(analysis) === 1;
}
