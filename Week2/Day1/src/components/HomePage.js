// src/components/HomePage.js
import React from 'react';
import Typography from '@mui/material/Typography';

export default function HomePage() {
  return (
    <div style={{ padding: '1rem' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to My Homepage
      </Typography>
      <Typography variant="body1">
        This homepage uses Material-UI Typography and AppBar.
      </Typography>
    </div>
  );
}
