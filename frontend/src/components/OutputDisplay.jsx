import React from 'react';
import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const OutputDisplay = () => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" component="h1" gutterBottom>
          Results Display
        </Typography>
        <Typography variant="body1" paragraph>
          View the generated SQL query and TRC explanation here.
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Button 
            variant="contained" 
            onClick={() => navigate('/query')}
            sx={{ mr: 2 }}
          >
            New Query
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

export default OutputDisplay;
