import gql from "graphql-tag";


export const createPostMutation = gql`
    mutation CreatePost($title: String, $content: String, $tags: TagInput!) {
        createPost(input: {title: $title, content: $content, tags: [$tags]}) {
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