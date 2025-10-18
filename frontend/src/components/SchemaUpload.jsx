import React from 'react';
import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const SchemaUpload = () => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" component="h1" gutterBottom>
          Schema Upload
        </Typography>
        <Typography variant="body1" paragraph>
          Upload your database schema in SQL DDL format to generate a Knowledge Graph.
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Button 
            variant="contained" 
            onClick={() => navigate('/query')}
            sx={{ mr: 2 }}
          >
            Upload Schema (Coming Soon)
          </Button>
          <Button 
            variant="outlined" 
            onClick={() => navigate('/query')}
          >
            Go to Query Input
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SchemaUpload;
