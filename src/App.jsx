import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState(null);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch Genre List on Load
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/genres')
      .then(response => setGenres(response.data))
      .catch(error => console.error("Error fetching genres:", error));
  }, []);

  // Handle Genre Click
  const handleGenreSelect = async (genre) => {
    setSelectedGenre(genre);
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/recommend?genre=${genre}`);
      setMovies(response.data);
    } catch (error) {
      console.error("Error fetching movies:", error);
    }
    setLoading(false);
  };

  return (
    <div className={`app-container ${selectedGenre ? 'layout-split' : 'layout-center'}`}>
      
      {/* LEFT SIDE (or Center initially) : Genre Picker */}
      <div className="genre-panel">
        <h1>Movie Recommender</h1>
        <p>Pick your mood</p>
        <div className="genre-list">
          {genres.map((genre) => (
            <button 
              key={genre} 
              className={`genre-btn ${selectedGenre === genre ? 'active' : ''}`}
              onClick={() => handleGenreSelect(genre)}
            >
              {genre}
            </button>
          ))}
        </div>
      </div>

      {/* RIGHT SIDE : Movie Results (Only visible after selection) */}
      {selectedGenre && (
        <div className="results-panel">
          <h2>Top picks for: <span>{selectedGenre}</span></h2>
          
          {loading ? (
            <div className="loading">Loading recommendations...</div>
          ) : (
            <div className="movie-grid">
              {movies.map((movie) => (
                <div key={movie.id} className="movie-card">
                  <img src={movie.poster_url} alt={movie.title} />
                  <div className="movie-info">
                    <h3>{movie.title}</h3>
                    <span className="rating">⭐ {movie.vote_average}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;