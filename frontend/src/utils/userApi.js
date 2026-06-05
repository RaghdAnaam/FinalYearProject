import requests from './requests';

export async function fetchCurrentUser() {
  const query = `
    query {
      currentUser {
        firstName
        lastName
        email
      }
    }
  `;
  const response = await requests(query);
  // LOG for debug
  console.log('FULL fetchCurrentUser RESPONSE:', response);

  // This is correct: response.data.data.currentUser is wrong! Use response.data.currentUser!
  return response?.data?.currentUser || null;
}
