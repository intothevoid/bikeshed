import Navbar from "./components/Navbar";
import Post from "./components/Post";
import data from './data';

function App() {
  // Get post data from posts.js
  const posts = data.map((item, id) => {
    return (
    <Post
      className='post'
      key={id}
      {...item}
    />
    )
  });

  return (
    <div>
      <Navbar />
      {posts}
    </div>
  );
}

export default App;
