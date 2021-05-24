/*
planning.js
dva model 数据交互
*/
import { message } from 'antd'

import {
  postChangeFlight,
  queryFromHost,
  postChangeMission
} from '../services/method'

export default {
  namespace: 'planning',
  state: {
    // mission_a: [],
    // mission_b: [],
    todo_list: [],
    position: [],
    flight_info: [
      {
        header: '0号无人机状态',
        key: '0',
        id: 'uav 0',
        position: '',
        status: ['', 'default'],
        battery: '',
        ma: '',
        mb: '',
        list: [],
        load: '',
        cost: ''
      }
    ],
    mission_info: [
      {
        header: '0号任务状态',
        key: '0',
        id: 'm 0',
        des: '',
        status: ['', 'default']
      }
    ],
    avail_mission: ['m 0']
  },
  effects: {
    *query_from_host({ payload }, sagaEffects) {
      //console.log(payload)
      const { call, put } = sagaEffects
      const response = yield call(queryFromHost, payload)
      //console.log(response)
      yield put({ type: 'Change', payload: response })
    },
    *post_change_flight({ payload }, sagaEffects) {
      //console.log("asdf")
      const { call, put } = sagaEffects
      const response = yield call(postChangeFlight, payload)
      //console.log(response)
      if (response['message'] == '个体动作配置信息已送达') {
        message.success(response['message'], 3)
      } else {
        message.error(response['message'], 3)
      }
      //yield put({ type: 'Change', payload: response })
    },
    *post_change_mission({ payload }, sagaEffects) {
      //console.log("asdf")
      const { call, put } = sagaEffects
      const response = yield call(postChangeMission, payload)
      //console.log(response)
      message.success(response['message'], 3)
      //yield put({ type: 'Change', payload: response })
    }
  },
  reducers: {
    Change(state, { payload: datasets }) {
      const next_todo_list = datasets['todo_list']
      const next_position = datasets['position']
      const next_flight_info = datasets['flight_info']
      const next_mission_info = datasets['mission_info']
      const next_avail_mission = datasets['avail_mission']
      return {
        todo_list: next_todo_list,
        position: next_position,
        flight_info: next_flight_info,
        mission_info: next_mission_info,
        avail_mission: next_avail_mission
      }
    }
  }
}
