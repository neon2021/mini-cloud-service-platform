import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';
const LAMBDA_BASE_URL = 'http://localhost:8001';

// EC2 Service API
export const ec2Service = {
  // 创建虚拟机
  createInstance: (data) => axios.post(`${API_BASE_URL}/instances`, data),
  
  // 获取虚拟机列表
  listInstances: () => axios.get(`${API_BASE_URL}/instances`),
  
  // 获取虚拟机详情
  getInstance: (name) => axios.get(`${API_BASE_URL}/instances/${name}`),
  
  // 启动虚拟机
  startInstance: (name) => axios.post(`${API_BASE_URL}/instances/${name}/actions`, { action: 'start' }),
  
  // 停止虚拟机
  stopInstance: (name) => axios.post(`${API_BASE_URL}/instances/${name}/actions`, { action: 'stop' }),
  
  // 删除虚拟机
  deleteInstance: (name) => axios.delete(`${API_BASE_URL}/instances/${name}`)
};

// Lambda Service API
export const lambdaService = {
  // 部署函数
  deployFunction: (data) => {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('runtime', data.runtime);
    formData.append('handler', data.handler);
    formData.append('code', data.code);
    formData.append('memory', data.memory || 128);
    formData.append('timeout', data.timeout || 30);
    return axios.post(`${LAMBDA_BASE_URL}/functions`, formData);
  },
  
  // 获取函数列表
  listFunctions: () => axios.get(`${LAMBDA_BASE_URL}/functions`),
  
  // 调用函数
  invokeFunction: (name) => 
    axios.post(`${LAMBDA_BASE_URL}/functions/${name}/invoke`, {}),
  
  // 删除函数
  deleteFunction: (name) => axios.delete(`${LAMBDA_BASE_URL}/functions/${name}`)
}; 