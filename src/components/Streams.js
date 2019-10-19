import React, { useEffect, useState } from "react";
import api from "../api";
function Stream() {
  const [channels, setChannels] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      const result = await api.get("https://api.twitch.tv/helix/streams");
      let dataArray = result.data.data;
      //console.log(dataArray);
      let gameIDs = dataArray.map(stream => {
        return stream.game_id;
      });
      //console.log(gameIDs);

      let baseURL = "https://api.twitch.tv/helix/games?";
      let queryParams = "";
      gameIDs.map(id => {
        return (queryParams = queryParams + `id=${id}&`);
      });

      let finalURL = baseURL + queryParams;
      let gameNames = await api.get(finalURL);
      let gameNameArray = gameNames.data.data;

      let finalArray = dataArray.map(stream => {
        stream.gameName = "";
        gameNameArray.map(name => {
          if (stream.game_id === name.id) {
            return (stream.gameName = name.name);
          }
        });

        let newURL = stream.thumbnail_url
          .replace("{width}", "300")
          .replace("{height}", "300");
        stream.thumbnail_url = newURL;
        return stream;
      });
      setChannels(finalArray);
    };
    fetchData();
  }, []);
  return (
    <div>
      <h1>Most Popular Live Streams</h1>
      <div className="row">
        {channels.map(channel => (
          <div className="col-lg-4 col-md-6 col-sm-12 mt-5">
            <div className="card">
              <img className="card-img-top" src={channel.thumbnail_url} />
              <div className="card-body">
                <h3 className="card-title">{channel.user_name}</h3>
                <h5 className="card-text"> {channel.gameName}</h5>
                <div className="card-text">
                  {channel.viewer_count} live viewers
                </div>
                <button className="btn btn-success">
                  <a
                    href={"https://twitch.tv/" + channel.user_name}
                    className="link"
                    target="_blank"
                  >
                    watch {channel.user_name}'s' stream
                  </a>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Stream;
