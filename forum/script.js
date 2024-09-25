// Load posts from localStorage on page load
window.onload = function() {
  loadPosts();
};

// Function to create a new post
function createPost() {
  const title = document.getElementById('post-title').value;
  const content = document.getElementById('post-content').value;

  if (title && content) {
    const post = {
      id: Date.now(),
      title: title,
      content: content,
      comments: []
    };
    
    let posts = JSON.parse(localStorage.getItem('posts')) || [];
    posts.push(post);
    localStorage.setItem('posts', JSON.stringify(posts));
    
    document.getElementById('post-title').value = '';
    document.getElementById('post-content').value = '';

    loadPosts();
  } else {
    alert('Vui lòng điền tiêu đề và nội dung bài viết.');
  }
}

// Function to load posts from localStorage
function loadPosts() {
  const postsContainer = document.getElementById('posts');
  postsContainer.innerHTML = ''; // Clear existing posts
  
  const posts = JSON.parse(localStorage.getItem('posts')) || [];
  
  posts.forEach(post => {
    const postDiv = document.createElement('div');
    postDiv.classList.add('post');
    
    postDiv.innerHTML = `
      <h3>${post.title}</h3>
      <p>${post.content}</p>
      <div class="comments" id="comments-${post.id}"></div>
      <textarea placeholder="Viết bình luận..." class="comment-input" id="comment-input-${post.id}"></textarea>
      <button class="submit-btn" onclick="addComment(${post.id})">Thêm bình luận</button>
    `;
    
    postsContainer.prepend(postDiv);
    loadComments(post);
  });
}

// Function to add a comment to a post
function addComment(postId) {
  const commentInput = document.getElementById(`comment-input-${postId}`);
  const commentText = commentInput.value;
  
  if (commentText) {
    let posts = JSON.parse(localStorage.getItem('posts')) || [];
    const post = posts.find(p => p.id === postId);
    
    post.comments.push(commentText);
    localStorage.setItem('posts', JSON.stringify(posts));
    
    commentInput.value = '';
    loadPosts();  // Reload posts to show new comment
  } else {
    alert('Vui lòng viết bình luận trước khi gửi.');
  }
}

// Function to load comments for a post
function loadComments(post) {
  const commentsDiv = document.getElementById(`comments-${post.id}`);
  commentsDiv.innerHTML = '';  // Clear existing comments

  post.comments.forEach(comment => {
    const commentDiv = document.createElement('div');
    commentDiv.classList.add('comment');
    commentDiv.textContent = comment;
    commentsDiv.appendChild(commentDiv);
  });
}
