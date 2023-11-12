import { Grid } from "@mui/material";
import ChatPage from "./ChatPage";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";


function App() {
  return (
    <Grid container spacing={1} style={{ height: "800px" }}>
      <Grid item xs={3} fullWidth>
        <ListItem component="div" disablePadding>
          <ListItemButton>
            <ListItemText primary={1} />
          </ListItemButton>
        </ListItem>
        <ListItem component="div" disablePadding>
          <ListItemButton>
            <ListItemText primary={1} />
          </ListItemButton>
        </ListItem>
        <ListItem component="div" disablePadding>
          <ListItemButton>
            <ListItemText primary={1} />
          </ListItemButton>
        </ListItem>
      </Grid>
      <Grid item xs={8} fullWidth>
        <ChatPage></ChatPage>
      </Grid>
    </Grid>
  );
}

export default App;
