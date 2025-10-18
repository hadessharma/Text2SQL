import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SchemaUpload from './components/SchemaUpload';
import QueryInput from './components/QueryInput';
import OutputDisplay from './components/OutputDisplay';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <h1 className="text-3xl font-bold text-gray-900">
                    Text2SQL System
                  </h1>
                </div>
              </div>
              <div className="text-sm text-gray-500">
                Natural Language to SQL Converter
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<SchemaUpload />} />
            <Route path="/query" element={<QueryInput />} />
            <Route path="/results" element={<OutputDisplay />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;