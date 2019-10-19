import axios from "axios";

//insert your Twitch API key into this variable for the project to works
let API_KEY = "";
let api = axios.create({
  headers: {
    "Client-ID": API_KEY
  }
});

export default api;
