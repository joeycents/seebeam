import React, { useState } from 'react';
import './App.css';
import CameraPermission from './components/CameraPermission';
import CalibrationScreen from './components/CalibrationScreen';
import ValidationScreen from './components/ValidationScreen';
import StudyInterface from './components/StudyInterface';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [stage, setStage] = useState('permission'); // permission, calibration, validation, study, results
  const [calibrationData, setCalibrationData] = useState(null);
  const [gazeData, setGazeData] = useState([]);

  const handlePermissionGranted = () => {
    setStage('calibration');
  };

  const handleCalibrationComplete = (data) => {
    setCalibrationData(data);
    setStage('validation');
  };

  const handleValidationComplete = () => {
    setStage('study');
  };

  const handleStudyComplete = (data) => {
    setGazeData(data);
    setStage('results');
  };

  const handleRestart = () => {
    setStage('permission');
    setCalibrationData(null);
    setGazeData([]);
  };

  return (
    <div className="App">
      {stage === 'permission' && (
        <CameraPermission onPermissionGranted={handlePermissionGranted} />
      )}

      {stage === 'calibration' && (
        <CalibrationScreen onComplete={handleCalibrationComplete} />
      )}

      {stage === 'validation' && (
        <ValidationScreen
          calibrationData={calibrationData}
          onComplete={handleValidationComplete}
          onFailed={() => setStage('calibration')}
        />
      )}

      {stage === 'study' && (
        <StudyInterface
          calibrationData={calibrationData}
          onComplete={handleStudyComplete}
        />
      )}

      {stage === 'results' && (
        <ResultsDashboard
          gazeData={gazeData}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
}

export default App;
