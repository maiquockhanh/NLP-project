import "./App.css";
import axios from "axios";
import {
  TextField,
  Button,
  Card,
  List,
  ListItem,
  CardActionArea,
  Typography,
  CardContent,
  Box,
  LinearProgress,
  Link,
  Slider,
} from "@mui/material";
import React, { useState, useEffect } from "react";

const modelEndPoint = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [numSearchRes, setNumSearchRes] = useState(5);
  const [links, setLinks] = useState(null);
  const [resultPercent, setResultPercent] = useState(null);
  const [sortedKey, setSortedKey] = useState(null);
  const [isSort, setIsSort] = useState(false);

  useEffect(() => {}, [links]);

  const executeQuery = async (query, num) => {
    setResultPercent(null);
    setLinks(null);
    setIsSort(false);
    setSortedKey(null);
    const response = await axios.get(
      `${modelEndPoint}/search/?q=${query}&n=${num}`
    );
    // console.log(response.data.link);
    setLinks(response.data.link);
    evaluate(response.data.link);
  };

  const sortKey = (list) => {
    var arr = [];
    console.log(list);
    for (var item in list) {
      arr.push(list[item]["sorted_key_list"]);
    }
    return arr;
  };

  const evaluate = async (link_list) => {
    var links_param = [];
    for (let index = 0; index < Object.values(link_list).length; index++) {
      links_param.push(link_list[index]);
    }
    await axios
      .post(`${modelEndPoint}/evaluate`, {
        links: links_param,
        query: query,
      })
      .then((result) => {
        setResultPercent(JSON.parse(result.data[0]));
        console.log(JSON.parse(result.data[0]));
        const arr = sortKey(JSON.parse(result.data[0]));
        setSortedKey(arr);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const _handleTextFieldChange = (e) => {
    setQuery(e.target.value);
  };

  const _handleSliderChange = (event, newValue) => {
    setNumSearchRes(newValue);
  };

  const sort = () => {
    setIsSort(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <TextField
          sx={{ mb: 2, mt: 5, width: "70%" }}
          id="outlined-basic"
          label="Query"
          multiline
          maxRows={5}
          value={query}
          onChange={_handleTextFieldChange}
        />
        <Box
          sx={{ width: "30%", display: "flex", flexDirection: "row" }}
          alignItems="center"
        >
          <Typography variant="body2" color="text.secondary">
            Number of search results
          </Typography>
          <Slider
            sx={{ m: 2 }}
            aria-label="Volume"
            value={numSearchRes}
            onChange={_handleSliderChange}
          />
          <Typography variant="body2" color="text.secondary">
            {numSearchRes}
          </Typography>
        </Box>
        <Box>
          <Button
            sx={{ mr: 2 }}
            variant="contained"
            onClick={() => executeQuery(query, numSearchRes)}
          >
            Execute
          </Button>
          <Button variant="contained" onClick={sort}>
            Sort
          </Button>
        </Box>
        {links && (
          <List sx={{ width: "70%" }}>
            {(isSort ? sortedKey : Object.keys(links)).map((value) => (
              <ListItem key={value} disableGutters>
                <Card sx={{ width: "100%" }} variant="outlined">
                  <Link
                    href={links[value]}
                    underline="none"
                    rel="noopener noreferrer"
                    target="_blank"
                  >
                    <CardActionArea>
                      <Box
                        sx={{ display: "flex", flexDirection: "row" }}
                        alignItems="center"
                      >
                        <CardContent sx={{ width: "80%" }}>
                          <Typography variant="body2" color="text.secondary">
                            {links[value]}
                          </Typography>
                        </CardContent>
                        {resultPercent ? (
                          <Box sx={{ width: "20%", mr: 2 }}>
                            <LinearProgress
                              variant="determinate"
                              value={resultPercent[value]["percentage"] * 100}
                            />
                            <Typography
                              variant="body2"
                              color="text.secondary"
                            >{`${Math.round(
                              resultPercent[value]["percentage"] * 100
                            )}%`}</Typography>
                          </Box>
                        ) : (
                          <LinearProgress sx={{ width: "20%", mr: 4 }} />
                        )}
                      </Box>
                    </CardActionArea>
                  </Link>
                </Card>
              </ListItem>
            ))}
          </List>
        )}
      </header>
    </div>
  );
}

export default App;
