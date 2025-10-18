import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const OutputDisplay = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('sql');

  // Mock data - replace with actual API response
  const mockData = {
    originalQuery: "Show me all users who made orders in the last month",
    sqlQuery: `SELECT DISTINCT u.id, u.name, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
ORDER BY u.name;`,
    trcExplanation: `This query retrieves user information for customers who have placed orders in the last month.

Key components:
• SELECT DISTINCT u.id, u.name, u.email - Returns unique user details
• FROM users u - Main table containing user information
• INNER JOIN orders o ON u.id = o.user_id - Links users with their orders
• WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH) - Filters for recent orders
• ORDER BY u.name - Sorts results alphabetically by user name

The query ensures we only get users who have actually made purchases recently, excluding inactive users.`,
    executionTime: "0.023s",
    rowsAffected: 47
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-xl shadow-xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Query Results
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Your natural language query has been converted to SQL. Review the results below.
          </p>
        </div>

        {/* Original Query */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Original Query</h2>
          <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
            <p className="text-gray-800 italic">"{mockData.originalQuery}"</p>
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
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Generated SQL
              </button>
              <button
                onClick={() => setActiveTab('explanation')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'explanation'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                TRC Explanation
              </button>
              <button
                onClick={() => setActiveTab('execution')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'execution'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Execution Info
              </button>
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="mb-8">
          {activeTab === 'sql' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Generated SQL Query</h3>
                <button
                  onClick={() => copyToClipboard(mockData.sqlQuery)}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Copy SQL
                </button>
              </div>
              <div className="bg-gray-900 rounded-lg p-6 overflow-x-auto">
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                  {mockData.sqlQuery}
                </pre>
              </div>
            </div>
          )}

          {activeTab === 'explanation' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">TRC Explanation</h3>
              <div className="bg-blue-50 rounded-lg p-6">
                <div className="prose prose-blue max-w-none">
                  <p className="text-gray-800 whitespace-pre-line">{mockData.trcExplanation}</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'execution' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Execution Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-green-50 rounded-lg p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg font-medium text-green-900">Execution Time</h4>
                      <p className="text-2xl font-bold text-green-600">{mockData.executionTime}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-blue-50 rounded-lg p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg font-medium text-blue-900">Rows Returned</h4>
                      <p className="text-2xl font-bold text-blue-600">{mockData.rowsAffected}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/query')}
            className="px-8 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 focus:ring-4 focus:ring-purple-200 transition-colors"
          >
            New Query
          </button>
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:ring-4 focus:ring-gray-200 transition-colors"
          >
            Back to Schema Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default OutputDisplay;
