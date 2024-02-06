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

export const createTagMutation = gql`
    mutation createTag($name: String!) {
        createTag(input: {name: $name}) {
            errors {
                messages
                field
            }
            tag {
                id
                name
            }
        }
    }
`

export const createCommentMutation = gql`
    mutation CreateComment($slug: String!, $comment: String!) {
        createComment(inputs: {
            postSlug: $slug, 
            comment: $comment, 
        }) {
            success
        }
    }
`

export const deleteCommentMutation = gql`
    mutation deleteComment($id: Int!) {
        deleteComment(id: $id) {
            success
        }
    }
`

export const updateCommentMutation = gql`
    mutation updateComment($id: Int!, $comment: String!) {
        updateComment(id: $id, comment: $comment) {
        success
        }
    }
`