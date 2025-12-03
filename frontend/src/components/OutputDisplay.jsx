import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { format } from 'sql-formatter';

const OutputDisplay = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [activeTab, setActiveTab] = useState('sql');

  // Pull API response from navigation state
  const responseData = location.state?.response;
  const databaseId = location.state?.database_id;

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
          onClick={() => navigate('/query', { state: { database_id: databaseId } })}
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

  const formattedSql = responseData.sql_query ? format(responseData.sql_query, { language: 'postgresql' }) : '';

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
                className={`py-2 px-1 border-b-2 font-medium text-sm ${activeTab === 'sql'
                  ? 'border-purple-500 text-purple-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
              >
                Generated SQL
              </button>

              <button
                onClick={() => setActiveTab('explanation')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${activeTab === 'explanation'
                  ? 'border-purple-500 text-purple-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
              >
                TRC Explanation
              </button>

              <button
                onClick={() => setActiveTab('validation')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${activeTab === 'validation'
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
                  onClick={() => copyToClipboard(formattedSql)}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center"
                >
                  Copy SQL
                </button>
              </div>

              <div className="bg-gray-900 rounded-lg p-6 overflow-x-auto">
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                  {formattedSql}
                </pre>
              </div>
            </div>
          )}

          {activeTab === 'explanation' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Tuple Relational Calculus Explanation</h3>

              <div className="space-y-6">
                {/* Formal Notation Card */}
                <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
                  <div className="bg-purple-50 px-6 py-4 border-b border-purple-100">
                    <h4 className="font-bold text-purple-800 flex items-center">
                      <span className="text-xl mr-2">∑</span> Formal Notation
                    </h4>
                  </div>
                  <div className="p-6 bg-gray-50">
                    <code className="text-lg font-mono text-purple-700 bg-white px-4 py-2 rounded border border-purple-200 block w-full overflow-x-auto">
                      {responseData.trc_explanation.trc}
                    </code>
                  </div>
                </div>

                {/* English Description Card */}
                <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
                  <div className="bg-blue-50 px-6 py-4 border-b border-blue-100">
                    <h4 className="font-bold text-blue-800 flex items-center">
                      <span className="text-xl mr-2">ℹ️</span> English Description
                    </h4>
                  </div>
                  <div className="p-6">
                    <p className="text-gray-700 text-lg leading-relaxed">
                      {responseData.trc_explanation.description}
                    </p>
                  </div>
                </div>

                {/* SQL Mapping Card */}
                <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
                  <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                    <h4 className="font-bold text-gray-700 flex items-center">
                      <span className="text-xl mr-2">🔄</span> SQL Mapping
                    </h4>
                  </div>
                  <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Original Query</span>
                      <p className="mt-1 text-gray-900 font-medium">"{responseData.trc_explanation.query}"</p>
                    </div>
                    <div>
                      <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Generated SQL</span>
                      <code className="mt-1 block text-sm font-mono text-gray-600 bg-gray-100 p-2 rounded">
                        {responseData.trc_explanation.sql}
                      </code>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'validation' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Validation Pipeline Results</h3>

              <div className="space-y-4">
                {/* Syntactic Validation */}
                <div className={`p-4 rounded-lg border ${responseData.validation_status.syntactic?.valid ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-900">1. Syntactic Validation</h4>
                    <span className="text-xl">{responseData.validation_status.syntactic?.valid ? '✅' : '❌'}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">Checks for valid SQL syntax.</p>
                  {responseData.validation_status.syntactic?.errors?.length > 0 && (
                    <ul className="list-disc ml-5 text-sm text-red-700">
                      {responseData.validation_status.syntactic.errors.map((err, i) => <li key={i}>{err}</li>)}
                    </ul>
                  )}
                </div>

                {/* Semantic Validation */}
                <div className={`p-4 rounded-lg border ${responseData.validation_status.semantic?.valid ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-900">2. Semantic Validation</h4>
                    <span className="text-xl">{responseData.validation_status.semantic?.valid ? '✅' : '❌'}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">Checks against Knowledge Graph schema.</p>
                  {responseData.validation_status.semantic?.errors?.length > 0 && (
                    <ul className="list-disc ml-5 text-sm text-red-700">
                      {responseData.validation_status.semantic.errors.map((err, i) => <li key={i}>{err}</li>)}
                    </ul>
                  )}
                </div>

                {/* Logical Validation */}
                <div className={`p-4 rounded-lg border ${responseData.validation_status.logical?.valid ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-900">3. Logical & Security Validation</h4>
                    <span className="text-xl">{responseData.validation_status.logical?.valid ? '✅' : '❌'}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">Checks for allowed operations and security rules.</p>
                  {responseData.validation_status.logical?.errors?.length > 0 && (
                    <ul className="list-disc ml-5 text-sm text-red-700">
                      {responseData.validation_status.logical.errors.map((err, i) => <li key={i}>{err}</li>)}
                    </ul>
                  )}
                </div>

                {/* Overall Status */}
                <div className="mt-6 p-4 bg-gray-100 rounded-lg text-center">
                  <span className="font-bold text-gray-700">Overall Status: </span>
                  <span className={`font-bold ${responseData.validation_status.overall_valid ? 'text-green-600' : 'text-red-600'}`}>
                    {responseData.validation_status.overall_valid ? 'PASSED' : 'FAILED'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/query', { state: { database_id: databaseId } })}
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
