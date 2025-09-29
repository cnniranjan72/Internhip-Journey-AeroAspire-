// src/components/AppBar.js
import React from 'react';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export default function AppBar() {
  return (
    <MuiAppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div">
          My MUI App
        </Typography>
      </Toolbar>
    </MuiAppBar>
  );
}
