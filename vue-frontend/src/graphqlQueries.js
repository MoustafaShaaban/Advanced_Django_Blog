import gql from "graphql-tag";

export const getAllPosts = gql`
    query ReturnAllPosts {
      allPosts {
        id
        slug
        title
        author {
          username
          avatar
        }
        favorites {
          username
        }
        likes {
          username
        }
        content
        updatedAt
        publishedAt
        comments {
          id
          comment
          publishedAt
          user {
            username
          }
        }
        tag {
          id
          name
        }
      }
    }
`;

export const getPostBySlug = gql`
    query returnPostBySlug($slug: String!) {
      postBySlug(slug: $slug) {
        id
        title
        content
        author {
          username
          avatar
        }
        updatedAt
        comments {
          id
          comment
          user {
            username
          }
        }
        tag {
          id
          name
        }
      }
    }
`

export const getUserPosts = gql`
query ReturnMyPost {
    myPostsWithFilters {
        edges {
            node {
                id
                title
                content
                updatedAt
                comment {
                    id
                    comment
                    email
                user {
                    username
                }
                }
                tag {
                    id
                    name
                }
            }
        }
    }
}
`

export const getAllTags = gql`
  query allTags {
    allTags {
      id
      name
      slug
    }
  }
`

export const getCommentById = gql`
  query getCommentById($id: Int!) {
    commentById(id: $id) {
      id
      user {
        username
      }
      comment
    }
  }
`

export const filterPostsByTitle = gql`
  query postFilters($title: String!, $limit: Int) {
    allPostsWithFilters(title_Icontains: $title, first: $limit) {
      edges {
        node {
          title
          slug
          author {
            username
          }
          publishedAt
          updatedAt
          content
          comments {
            id
            user {
              username
            }
            comment
          }
          tag {
            id
            name
          }
        }
      }
    }
  }
`

export const userFavoritePostsList = gql`
  query {
    userFavoritePosts {
      title
      slug
      author {
        username
      }
      content
      tag {
        id
        name
      }
      publishedAt
      updatedAt
      slug
      favorites {
        username
      }
      comments {
        id
        user {
          username
        }
        comment
      }
    }
  }
`

export const userPostsList = gql`
  query {
    userPosts {
      title
      slug
      author {
        username
      }
      content
      tag {
        id
        name
      }
      publishedAt
      updatedAt
      slug
      favorites {
        username
      }
      comments {
        id
        user {
          username
        }
        comment
      }
    }
  }
`
