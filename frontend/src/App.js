import React, { useState } from 'react';
import './App.css';
import CameraPermission from './components/CameraPermission';
import PositionCheck from './components/PositionCheck';
import CalibrationScreen from './components/CalibrationScreen';
import ValidationScreen from './components/ValidationScreen';
import ReValidation from './components/ReValidation';
import LargeGrid from './components/LargeGrid';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  // Flow: permission → position → calibration → validation → revalidation1 → largegrid → revalidation2 → results
  const [stage, setStage] = useState('permission');
  const [calibrationData, setCalibrationData] = useState(null);
  const [firstReValidationData, setFirstReValidationData] = useState(null);
  const [largeGridData, setLargeGridData] = useState(null);
  const [secondReValidationData, setSecondReValidationData] = useState(null);

  const handlePermissionGranted = () => {
    setStage('position');
  };

  const handlePositionConfirmed = () => {
    setStage('calibration');
  };

  const handleCalibrationComplete = (data) => {
    setCalibrationData(data);
    setStage('validation');
  };

  const handleValidationComplete = () => {
    setStage('revalidation1');
  };

  const handleFirstReValidationComplete = (data) => {
    setFirstReValidationData(data);
    setStage('largegrid');
  };

  const handleLargeGridComplete = (data) => {
    setLargeGridData(data);
    setStage('revalidation2');
  };

  const handleSecondReValidationComplete = (data) => {
    setSecondReValidationData(data);
    setStage('results');
  };

  const handleRestart = () => {
    setStage('permission');
    setCalibrationData(null);
    setFirstReValidationData(null);
    setLargeGridData(null);
    setSecondReValidationData(null);
  };

  return (
    <div className="App">
      {stage === 'permission' && (
        <CameraPermission onPermissionGranted={handlePermissionGranted} />
      )}

      {stage === 'position' && (
        <PositionCheck onPositionConfirmed={handlePositionConfirmed} />
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

      {stage === 'revalidation1' && (
        <ReValidation
          onComplete={handleFirstReValidationComplete}
          isFirstValidation={true}
        />
      )}

      {stage === 'largegrid' && (
        <LargeGrid
          onComplete={handleLargeGridComplete}
        />
      )}

      {stage === 'revalidation2' && (
        <ReValidation
          onComplete={handleSecondReValidationComplete}
          isFirstValidation={false}
        />
      )}

      {stage === 'results' && (
        <ResultsDashboard
          calibrationData={calibrationData}
          firstReValidationData={firstReValidationData}
          largeGridData={largeGridData}
          secondReValidationData={secondReValidationData}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
}

export default App;
