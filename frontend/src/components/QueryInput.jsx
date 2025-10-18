import React from 'react';
import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const QueryInput = () => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" component="h1" gutterBottom>
          Query Input
        </Typography>
        <Typography variant="body1" paragraph>
          Enter your natural language query to convert it to SQL.
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Button 
            variant="contained" 
            onClick={() => navigate('/results')}
            sx={{ mr: 2 }}
          >
            Generate SQL (Coming Soon)
          </Button>
          <Button 
            variant="outlined" 
            onClick={() => navigate('/')}
          >
            Back to Schema Upload
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default QueryInput;
