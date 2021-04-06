/*
Amap.js
前端主界面
*/
import React, { Component } from 'react'
import { Map, MouseTool, Marker, Polyline } from 'react-amap'
import { connect } from 'dva'
import {
  Button,
  Card,
  Row,
  Col,
  Tabs,
  Tooltip,
  List,
  Layout,
  Form,
  Collapse,
  Descriptions,
  Badge,
  Space,
  Input,
  Select,
} from 'antd'
import {
  MinusCircleOutlined,
  PlusOutlined,
  createFromIconfontCN,
} from '@ant-design/icons'
import load_point from '../resources/load_point'

const IconFont0 = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1282563_kns8e1am00d.js',
})

const IconFont1 = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1289406_de15s4r5mdv.js',
})

const { TabPane } = Tabs
const { Header, Content, Footer } = Layout
const { Panel } = Collapse
const { Option } = Select

const namespace = 'planning'

const mapStateToProps = ({ [namespace]: n }) => {
  return {
    tInfo: n.todo_list,
    pInfo: n.position,
    fInfo: n.flight_info,
    mInfo: n.mission_info,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    query_from_host: () => {
      const action = {
        type: `${namespace}/query_from_host`,
        payload: {
          type: 0,
        },
      }
      dispatch(action)
    },
    post_change_flight: (values) => {
      const action = {
        type: `${namespace}/post_change_flight`,
        payload: {
          type: 1,
          ...values,
        },
      }
      dispatch(action)
    },
    post_change_mission: (values) => {
      const action = {
        type: `${namespace}/post_change_mission`,
        payload: {
          type: 2,
          ...values,
        },
      }
      dispatch(action)
    },
  }
}

@connect(mapStateToProps, mapDispatchToProps)
export default class Amap extends Component {
  constructor() {
    super()
    const self = this
    this.timer
    this.state = {
      what: '点击下方按钮开始绘制',
      load_point,
      color: [
        'black',
        'brown',
        'green',
        'red',
        'blue',
        'yellow',
        'purple',
        'orange',
      ],
    }
    this.amapEvents = {
      created: (mapInstance) => {
        self.map = mapInstance
      },
    }
    this.lineEvents = {
      created: (ins) => {
        console.log(ins)
      },
      show: () => {
        console.log('line show')
      },
    }
    this.toolEvents = {
      created: (tool) => {
        self.tool = tool
      },
      draw({ obj }) {
        self.drawWhat(obj)
      },
    }
    this.mapPlugins = ['ToolBar']
    this.mapCenter = { longitude: 118.957746, latitude: 32.115395 }
  }

  display() {
    let temp = []
    for (let a of this.props.pInfo.keys()) {
      temp = temp.concat({
        key: 'uav' + JSON.stringify(a),
        position: {
          longitude: this.props.pInfo[a][0] / 1000000,
          latitude: this.props.pInfo[a][1] / 1000000,
        },
      })
    }
    let temp_path = []
    let count_out = 0
    for (let a of this.props.tInfo) {
      let temptemp = []
      temptemp = temptemp.concat({
        longitude: this.props.pInfo[count_out][0] / 1000000,
        latitude: this.props.pInfo[count_out][1] / 1000000,
      })
      for (let b of a) {
        temptemp = temptemp.concat({
          longitude: this.state.load_point[b['point']].position.longitude,
          latitude: this.state.load_point[b['point']].position.latitude,
        })
      }
      temp_path = temp_path.concat({ route: temptemp, key: count_out })
      count_out += 1
    }
    return [temp, temp_path]
  }

  render() {
    const [load_uav, path] = this.display()
    const onChangeFlight = (values) => {
      this.props.post_change_flight(values)
    }
    const onChangeMission = (values) => {
      this.props.post_change_mission(values)
    }

    return (
      <div className="container">
        <div className="header">
          <div
            className="logo"
            style={{
              position: 'absolute',
              left: 50,
              textAlign: 'left',
              color: 'white',
              fontSize: 24,
            }}
          >
            <div>
              <IconFont0 style={{ padding: '20px' }} type="icon-wurenji-copy" />
              {`无人集群智能管控平台`}
            </div>
          </div>
        </div>
        <div className="content">
          <div className="my_map">
            <Map
              events={this.amapEvents}
              plugins={this.mapPlugins}
              center={this.mapCenter}
            >
              <MouseTool events={this.toolEvents} />
              {this.state.load_point.map((item) => (
                <Marker
                  position={item.position}
                  extData={{ key: item.key }}
                  clickable
                  title={item.key.toString()}
                  events={this.markerEvents}
                />
              ))}
              {load_uav.map((item) => (
                <Marker
                  position={item.position}
                  // icon={'//vdata.amap.com/icons/b18/1/2.png'}
                  offset={{ x: -8, y: -12 }}
                  title={item.key}
                >
                  <IconFont1 type="icon-wurenji" />
                </Marker>
              ))}
              {path.map((item) => (
                <Polyline
                  path={item.route}
                  showDir={true}
                  style={{
                    strokeWeight: 4,
                    strokeColor: this.state.color[item.key],
                  }}
                />
              ))}
            </Map>
          </div>
          <div className="my_manage">
            <Collapse defaultActiveKey={['0', '1']}>
              <Panel header="无人集群个体信息管理" key="0">
                <Collapse defaultActiveKey={['0']}>
                  {this.props.fInfo.map((v) => (
                    <Panel header={v['header']} key={v['key']}>
                      <Descriptions bordered>
                        <Descriptions.Item label="编号">
                          {v['id']}
                        </Descriptions.Item>
                        <Descriptions.Item label="位置" span={20}>
                          {v['position']}
                        </Descriptions.Item>
                        <Descriptions.Item label="状态">
                          <Badge
                            status={v['status'][1]}
                            text={v['status'][0]}
                          />
                        </Descriptions.Item>
                        <Descriptions.Item label="电量" span={20}>
                          {v['battery']}
                        </Descriptions.Item>
                        <Descriptions.Item label="待结束任务">
                          {v['ma']}
                        </Descriptions.Item>
                        <Descriptions.Item label="待开始任务" span={20}>
                          {v['mb']}
                        </Descriptions.Item>
                        <Descriptions.Item label="动作序列" span={20}>
                          {v['list']}
                        </Descriptions.Item>
                        <Descriptions.Item label="当前任务数">
                          {v['load']}
                        </Descriptions.Item>
                        <Descriptions.Item label="预计完成代价">
                          {v['cost']}
                        </Descriptions.Item>
                      </Descriptions>
                    </Panel>
                  ))}
                </Collapse>
              </Panel>
              <Panel header="任务信息管理" key="1">
                <Collapse defaultActiveKey={['0']}>
                  {this.props.mInfo.map((v) => (
                    <Panel header={v['header']} key={v['key']}>
                      <Descriptions bordered>
                        <Descriptions.Item label="编号">
                          {v['id']}
                        </Descriptions.Item>
                        <Descriptions.Item label="任务描述" span={20}>
                          {v['des']}
                        </Descriptions.Item>
                        <Descriptions.Item label="状态">
                          <Badge
                            status={v['status'][1]}
                            text={v['status'][0]}
                          />
                        </Descriptions.Item>
                      </Descriptions>
                    </Panel>
                  ))}
                </Collapse>
              </Panel>
            </Collapse>
          </div>
          <div className="my_control">
            <div className="my_start">
              <Button type="primary" htmlType="button">
                <a
                  onClick={(_) => {
                    clearInterval(this.timer)
                    this.timer = setInterval(() => {
                      this.props.query_from_host()
                    }, 100)
                  }}
                >
                  start
                </a>
              </Button>
            </div>
            <div className="my_interact">
              <div style={{ position: 'relative', left: '10%', width: '80%' }}>
                <Tabs defaultActiveKey="0" style={{ textAlign: 'center' }}>
                  <TabPane tab="无人集群个体动作配置" key="0">
                    <Form
                      name="dynamic_flights"
                      onFinish={onChangeFlight}
                      autoComplete="off"
                    >
                      <Form.List name="flights">
                        {(fields, { add, remove }) => (
                          <>
                            {fields.map((field) => (
                              <Space
                                key={field.key}
                                style={{ display: 'flex', marginBottom: 8 }}
                                align="baseline"
                              >
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'flight_id']}
                                  fieldKey={[field.fieldKey, 'flight_id']}
                                  rules={[
                                    {
                                      required: true,
                                      message: 'Missing flight id',
                                    },
                                  ]}
                                >
                                  <Select placeholder="flight id" allowClear>
                                    {this.props.fInfo.map((f) => (
                                      <Option value={f['id']}>{f['id']}</Option>
                                    ))}
                                  </Select>
                                </Form.Item>
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'point_id']}
                                  fieldKey={[field.fieldKey, 'point_id']}
                                  rules={[
                                    {
                                      required: true,
                                      message: 'Missing point id',
                                    },
                                  ]}
                                >
                                  <Input placeholder="point id" />
                                </Form.Item>
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'action']}
                                  fieldKey={[field.fieldKey, 'action']}
                                  rules={[
                                    {
                                      required: true,
                                      message: 'Missing action',
                                    },
                                  ]}
                                >
                                  <Input placeholder="action" />
                                </Form.Item>
                                <MinusCircleOutlined
                                  onClick={() => remove(field.name)}
                                />
                              </Space>
                            ))}
                            <Form.Item>
                              <Button
                                type="dashed"
                                onClick={() => add()}
                                block
                                icon={<PlusOutlined />}
                              >
                                添加无人机动作配置
                              </Button>
                            </Form.Item>
                          </>
                        )}
                      </Form.List>
                      <Form.Item>
                        <Button type="ghost" htmlType="submit">
                          Submit
                        </Button>
                      </Form.Item>
                    </Form>
                  </TabPane>
                  <TabPane tab="任务调整" key="1">
                    <Form
                      name="dynamic_missions"
                      onFinish={onChangeMission}
                      autoComplete="off"
                    >
                      <Form.List name="missions">
                        {(fields, { add, remove }) => (
                          <>
                            {fields.map((field) => (
                              <Space
                                key={field.key}
                                style={{ display: 'flex', marginBottom: 8 }}
                                align="baseline"
                              >
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'mission_id']}
                                  fieldKey={[field.fieldKey, 'mission_id']}
                                  rules={[
                                    {
                                      required: true,
                                      message: 'Missing mission id',
                                    },
                                  ]}
                                >
                                  <Select placeholder="mission id" allowClear>
                                    {this.props.mInfo.map((m) => (
                                      <Option value={m['id']}>{m['id']}</Option>
                                    ))}
                                  </Select>
                                </Form.Item>
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'action']}
                                  fieldKey={[field.fieldKey, 'action']}
                                  rules={[
                                    {
                                      required: true,
                                      message: 'Missing action',
                                    },
                                  ]}
                                >
                                  <Input placeholder="action" />
                                </Form.Item>
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'from_id']}
                                  fieldKey={[field.fieldKey, 'from_id']}
                                >
                                  <Input placeholder="from" />
                                </Form.Item>
                                <Form.Item
                                  {...field}
                                  name={[field.name, 'to_id']}
                                  fieldKey={[field.fieldKey, 'to_id']}
                                >
                                  <Input placeholder="to" />
                                </Form.Item>
                                <MinusCircleOutlined
                                  onClick={() => remove(field.name)}
                                />
                              </Space>
                            ))}
                            <Form.Item>
                              <Button
                                type="dashed"
                                onClick={() => add()}
                                block
                                icon={<PlusOutlined />}
                              >
                                添加任务调整
                              </Button>
                            </Form.Item>
                          </>
                        )}
                      </Form.List>
                      <Form.Item>
                        <Button type="ghost" htmlType="submit">
                          Submit
                        </Button>
                      </Form.Item>
                    </Form>
                  </TabPane>
                </Tabs>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
