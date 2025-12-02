import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const OutputDisplay = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [activeTab, setActiveTab] = useState('sql');

  // Pull API response from navigation state
  const responseData = location.state?.response;

  if (!responseData) {
    return (
      <div className="max-w-3xl mx-auto text-center mt-20">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          No Query Results Found
        </h1>
        <p className="text-gray-600 mb-8">
          Please run a query first.
        </p>
        <button
          onClick={() => navigate('/query')}
          className="px-6 py-3 bg-purple-600 text-white rounded-lg"
        >
          Go to Query Page
        </button>
      </div>
    );
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-xl shadow-xl p-8">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Query Results
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Your query has been processed and converted to SQL.
          </p>
        </div>

        {/* Original Query */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Original Query</h2>
          <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
            <p className="text-gray-800 italic">"{responseData.original_query}"</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('sql')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'sql'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                Generated SQL
              </button>

              <button
                onClick={() => setActiveTab('explanation')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'explanation'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                TRC Explanation
              </button>

              <button
                onClick={() => setActiveTab('validation')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'validation'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                Validation
              </button>
            </nav>
          </div>
        </div>

        {/* Output Tabs */}
        <div className="mb-8">
          {activeTab === 'sql' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Generated SQL Query</h3>
                <button
                  onClick={() => copyToClipboard(responseData.sql_query)}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center"
                >
                  Copy SQL
                </button>
              </div>

              <div className="bg-gray-900 rounded-lg p-6 overflow-x-auto">
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                  {responseData.sql_query}
                </pre>
              </div>
            </div>
          )}

          {activeTab === 'explanation' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Tuple Relational Calculus Explanation</h3>
              <div className="bg-blue-50 rounded-lg p-6">
                <p className="text-gray-800 whitespace-pre-line">
                  {responseData.trc_explanation}
                </p>
              </div>
            </div>
          )}

          {activeTab === 'validation' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Validation Results</h3>

              <div className="bg-gray-50 rounded-lg p-6">
                <pre className="text-gray-800 whitespace-pre-wrap text-sm">
                  {JSON.stringify(responseData.validation_status, null, 2)}
                </pre>

                {responseData.errors?.length > 0 && (
                  <div className="mt-4 bg-red-50 p-4 border-l-4 border-red-500 rounded-lg">
                    <h4 className="text-red-700 font-bold mb-2">Errors</h4>
                    <ul className="list-disc ml-6 text-red-700">
                      {responseData.errors.map((err, i) => (
                        <li key={i}>{err}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/query')}
            className="px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            New Query
          </button>
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
          >
            Back to Schema Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default OutputDisplay;
