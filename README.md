# Text2SQL Frontend

A modern React-based frontend for the Text2SQL system that converts natural language queries into SQL using Knowledge Graphs and Tuple Relational Calculus.

## 🚀 Quick Start

### Prerequisites

- **Node.js** (version 18 or higher)
- **npm** (comes with Node.js)

### Installation & Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173` to view the application.

## 🛠️ Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build production-ready application |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint for code quality checks |

## 🎨 Features

### Modern UI Components
- **Schema Upload**: Drag-and-drop SQL file upload with validation
- **Query Input**: Natural language query interface with examples
- **Results Display**: Tabbed view showing SQL, TRC explanation, and execution info
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### Key Functionality
- **File Upload**: Support for .sql and .txt files
- **Interactive Examples**: Clickable example queries for better UX
- **Real-time Validation**: Instant feedback on user input
- **Copy to Clipboard**: One-click SQL copying functionality
- **Loading States**: Visual feedback during API operations

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── SchemaUpload.jsx # Schema upload interface
│   │   ├── QueryInput.jsx   # Natural language input
│   │   └── OutputDisplay.jsx # Results display
│   ├── services/            # API services
│   │   └── api.js          # Backend API integration
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── package.json            # Dependencies and scripts
└── vite.config.js         # Vite configuration
```

## 🎯 User Workflow

1. **Schema Upload**: Upload your database schema in SQL DDL format
2. **Query Input**: Enter your natural language query
3. **Results**: View the generated SQL, TRC explanation, and execution details

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
```

### API Integration

The frontend communicates with the backend through the following endpoints:

- `POST /api/submit-schema`: Upload schema and generate Knowledge Graph
- `POST /api/generate-sql`: Process natural language query
