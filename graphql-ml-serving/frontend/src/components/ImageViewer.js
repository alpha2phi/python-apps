import { gql, useSubscription } from '@apollo/client';

const RECEIVE_MESSAGE = gql`
subscription messages($clientId: String!) {
  messages(clientId: $clientId) {
    content
    clientId
  }
}
`;

function ImageViewer({ clientId }) {
  const { data, loading, error } = useSubscription(RECEIVE_MESSAGE, { variables: { clientId: clientId } });
  if (loading) {
    return "";
  }
  if (error) {
    console.error(error);
    return <h4>Error processing</h4>;
  }
  var content = "";
  if (data) {
    content = data.messages.content;
  }
  return <img alt="result" src={content} width={"50%"} />
}

export default ImageViewer;
