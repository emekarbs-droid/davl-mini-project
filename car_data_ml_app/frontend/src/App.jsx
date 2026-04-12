import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import UploadPage from './pages/UploadPage';
import Dashboard from './pages/Dashboard';
import StatsPage from './pages/StatsPage';
import PreprocessingPage from './pages/PreprocessingPage';
import RegressionPage from './pages/RegressionPage';
import ClassificationPage from './pages/ClassificationPage';
import PcaPage from './pages/PcaPage';
import FeatureSelectionPage from './pages/FeatureSelectionPage';
import ClusteringPage from './pages/ClusteringPage';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  render() {
    if (this.state.hasError) {
      return (
        <div className="p-20 text-center">
          <h1 className="text-3xl font-bold text-red-600 mb-4">Application Crash</h1>
          <pre className="p-6 bg-gray-100 rounded-2xl text-left overflow-auto max-w-4xl mx-auto text-sm">
            {this.state.error?.toString()}
          </pre>
          <button onClick={() => window.location.reload()} className="mt-8 px-6 py-2 bg-blue-600 text-white rounded-xl">Reload System</button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50 text-gray-900 font-sans">
        <Sidebar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto">
          <ErrorBoundary>
            <Routes>
              <Route path="/" element={<UploadPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/stats" element={<StatsPage />} />
              <Route path="/preprocess" element={<PreprocessingPage />} />
              <Route path="/regression" element={<RegressionPage />} />
              <Route path="/classification" element={<ClassificationPage />} />
              <Route path="/pca" element={<PcaPage />} />
              <Route path="/feature-selection" element={<FeatureSelectionPage />} />
              <Route path="/clustering" element={<ClusteringPage />} />
            </Routes>
          </ErrorBoundary>
        </main>
      </div>
    </Router>
  );
}

export default App;
