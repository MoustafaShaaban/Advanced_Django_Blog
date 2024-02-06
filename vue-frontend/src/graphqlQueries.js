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
        content
        updatedAt
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
    query AllTags {
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