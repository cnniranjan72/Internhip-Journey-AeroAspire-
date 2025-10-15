import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Tooltip, Button, Box } from '@mui/material';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import AddTaskIcon from '@mui/icons-material/AddTask';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import { Link, useLocation } from 'react-router-dom';

export default function NavBar({ mode = 'light', onToggleTheme, token, onLogout }) {
  const location = useLocation();

  const navItems = [
    { to: '/', label: 'Home', icon: <HomeIcon fontSize="small" /> },
    { to: '/add', label: 'Add Task', icon: <AddTaskIcon fontSize="small" /> },
    { to: '/about', label: 'About', icon: <InfoIcon fontSize="small" /> },
  ];

  return (
    <AppBar position="static" color="primary" enableColorOnDark>
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/"
          sx={{ color: 'inherit', textDecoration: 'none', mr: 2 }}
        >
          Niranjan's Tasks
        </Typography>

        <Box sx={{ display: 'flex', gap: 1, flexGrow: 1 }}>
          {navItems.map((it) => {
            const active = location.pathname === it.to;
            return (
              <Button
                key={it.to}
                component={Link}
                to={it.to}
                startIcon={it.icon}
                color={active ? 'secondary' : 'inherit'}
                sx={{
                  textTransform: 'none',
                  fontWeight: active ? 700 : 500,
                }}
              >
                {it.label}
              </Button>
            );
          })}
        </Box>

        {/* Theme toggle */}
        <Tooltip title={`Switch to ${mode === 'light' ? 'dark' : 'light'} mode`}>
          <IconButton color="inherit" onClick={onToggleTheme}>
            {mode === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
          </IconButton>
        </Tooltip>

        {/* Login / Logout buttons */}
        {token ? (
          <Button color="inherit" onClick={onLogout} sx={{ ml: 1 }}>
            Logout
          </Button>
        ) : (
          <Button
            color="inherit"
            component={Link}
            to="/login"
            sx={{ ml: 1 }}
          >
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
}
