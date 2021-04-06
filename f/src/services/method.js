/*
method.js
自定义post
*/
import request from '../utils/request'

export async function queryFromHost(params) {
  //debugger
  //const reqHeader = getAuthRequestHeader()
  return request('/dev/', {
    method: 'POST',
    // timeout: 180000,
    // headers: {
    //   hi: "hello"
    // },
    body: JSON.stringify(params),
  })
}

export async function postChangeFlight(params) {
  //debugger
  //const reqHeader = getAuthRequestHeader()
  return request('/dev/', {
    method: 'POST',
    // timeout: 180000,
    // headers: {
    //   hi: "hello"
    // },
    body: JSON.stringify(params),
  })
}

export async function postChangeMission(params) {
  //debugger
  //const reqHeader = getAuthRequestHeader()
  return request('/dev/', {
    method: 'POST',
    // timeout: 180000,
    // headers: {
    //   hi: "hello"
    // },
    body: JSON.stringify(params),
  })
}

// export async function getTheRoute() {
//   //const reqHeader = getAuthRequestHeader()
//   return request('/dev/',{
//     method: 'GET',
//   });
// }
