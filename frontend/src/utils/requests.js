import axios from 'axios';

export default async function requests(query, options = {}) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await axios.post(
      'http://localhost:5001/graphql/',
      {
        query,
        variables: options.variables || {}
      },
      {
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        }
      }
    );

    // Return data in the format the components expect
    if (response.data.errors) {
      throw new Error(response.data.errors[0].message);
    }

    return {
      data: response.data.data
    };

  } catch (error) {
    console.error('GraphQL Error:', error);
    throw error;
  }
}
