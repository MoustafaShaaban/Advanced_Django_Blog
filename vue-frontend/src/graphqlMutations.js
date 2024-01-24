import gql from "graphql-tag";


export const createPostMutation = gql`
    mutation CreatePost($title: String, $content: String, $tags: [Int]!) {
        createPost(input: {title: $title, content: $content, tags: $tags}) {
            post {
                id
                title
                content
                tag {
                    name
                }
            }
        }
    }
`

export const updatePostMutation = gql`
    mutation UpdatePost($id: Int!, $title: String, $content: String, $tags: [Int]!) {
        updatePost(id: $id, input: {title: $title, content: $content, tags: $tags}) {
            post {
                id
                title
                content
                tag {
                    name
                }
            }
        }
    }
`

export const deletePostMutation = gql`
    mutation deletePost($id: Int!) {
        deletePost(id: $id) {
            success
        }
    }
`

// export const createPostMutation = gql`
//     mutation CreatePost($title:String!, $content: String!, $tags: Int!) {
//         createPost(input: {
//             title: $title,
//             content: $content
//             tags: $tags
            
//         }) {
//             success
//             post {
//                 id
//                 title
//                 content
//             }
//         }
//     }
// `