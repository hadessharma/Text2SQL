import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const QueryInput = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [query, setQuery] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [databaseId, setDatabaseId] = useState(null);

  useEffect(() => {
    if (location.state?.database_id) {
      setDatabaseId(location.state.database_id);
      console.log("Using Database ID:", location.state.database_id);
    } else {
      console.warn("No Database ID found in navigation state.");
      // Optional: Redirect back to upload if no ID? 
      // navigate('/'); 
    }
  }, [location.state, navigate]);

  const exampleQueries = [
    "Show me all users who made orders in the last month",
    "Find the top 10 customers by total order amount",
    "List all products that are out of stock",
    "Get the average order value by month",
    "Show me users who haven't placed any orders"
  ];

  const handleGenerateSQL = async () => {
    if (!query.trim()) return;

    setIsGenerating(true);
    try {
      if (!databaseId) {
        alert("No Database ID found. Please upload a schema first.");
        return;
      }

      console.log('Generating SQL for query:', query, 'with DB ID:', databaseId);

      const response = await fetch('http://localhost:8000/api/generate-sql', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          database_id: databaseId,
          user_query: query
        }),
      });

      if (response.ok) {
        const data = await response.json();
        navigate('/results', { state: { response: data, database_id: databaseId } });
      } else {
        console.error('Failed to generate SQL');
      }
    } catch (error) {
      console.error("Error generating SQL:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Natural Language Query
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Describe what you want to find in plain English, and we'll convert it to SQL for you.
          </p>
        </div>

        {/* Query Input */}
        <div className="mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Query
          </label>
          <div className="relative">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Show me all users who made orders in the last month"
              className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none text-lg"
            />
            <div className="absolute bottom-3 right-3 text-sm text-gray-400">
              {query.length}/500
            </div>
          </div>
        </div>

        {/* Example Queries */}
        <div className="mb-8">
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Try these examples:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="text-left p-3 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <button
            onClick={handleGenerateSQL}
            disabled={!query.trim() || isGenerating}
            className="px-8 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 focus:ring-4 focus:ring-green-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {isGenerating ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating SQL...
              </>
            ) : (
              'Generate SQL'
            )}
          </button>
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:ring-4 focus:ring-gray-200 transition-colors"
          >
            Back to Schema Upload
          </button>
        </div>

        {/* Tips Section */}
        <div className="bg-green-50 rounded-lg p-6">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="w-5 h-5 text-green-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800 mb-2">
                Tips for Better Results
              </h3>
              <div className="text-sm text-green-700 space-y-1">
                <p>• Be specific about what data you want to see</p>
                <p>• Mention table names if you know them (e.g., "users", "orders")</p>
                <p>• Include time ranges when relevant (e.g., "last month", "this year")</p>
                <p>• Specify sorting or grouping if needed (e.g., "top 10", "group by")</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QueryInput;
