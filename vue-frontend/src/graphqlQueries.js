import gql from "graphql-tag";

export const getAllPosts = gql`
    query ReturnAllPosts {
        allPosts {
                id
                title
                content
                updatedAt
                author {
                    username,
                    avatar
                }
                tag {
                    id
                    name
                }
        }
    }
`;

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