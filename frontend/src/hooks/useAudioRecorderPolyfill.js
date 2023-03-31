const useAudioRecorderPolyfill = () => {
    let AudioRecorder;
  
    if (typeof window !== 'undefined') {
      AudioRecorder = require('audio-recorder-polyfill');
    }
  
    return AudioRecorder;
  };
  
  export default useAudioRecorderPolyfill;
  