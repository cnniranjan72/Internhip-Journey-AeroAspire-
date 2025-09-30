import { createTheme } from '@mui/material/styles';

export default function themeBuilder(mode = 'light') {
  const isLight = mode === 'light';
  return createTheme({
    palette: {
      mode,
      primary: {
        main: isLight ? '#1976d2' : '#90caf9',
      },
      secondary: {
        main: isLight ? '#f50057' : '#f48fb1',
      },
      background: {
        default: isLight ? '#f5f7fb' : '#121212',
        paper: isLight ? '#ffffff' : '#1e1e1e',
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 12,
          },
        },
      },
      MuiButton: {
        defaultProps: {
          disableElevation: true,
        },
      },
    },
  });
}
