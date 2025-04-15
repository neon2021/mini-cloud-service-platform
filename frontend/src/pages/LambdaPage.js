import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  Space, 
  message,
  Tag,
  Popconfirm,
  Card
} from 'antd';
import { 
  PlusOutlined, 
  PlayCircleOutlined, 
  DeleteOutlined 
} from '@ant-design/icons';
import { lambdaService } from '../services/api';

const LambdaPage = () => {
  const [functions, setFunctions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  // 获取函数列表
  const fetchFunctions = async () => {
    try {
      setLoading(true);
      const response = await lambdaService.listFunctions();
      setFunctions(response.data);
    } catch (error) {
      message.error('获取函数列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFunctions();
  }, []);

  // 部署函数
  const handleDeploy = async (values) => {
    try {
      await lambdaService.deployFunction(values);
      message.success('函数部署成功');
      setModalVisible(false);
      form.resetFields();
      fetchFunctions();
    } catch (error) {
      message.error('函数部署失败');
    }
  };

  // 调用函数
  const handleInvoke = async (name) => {
    try {
      const response = await lambdaService.invokeFunction(name);
      message.success(`函数调用成功: ${response.data}`);
    } catch (error) {
      message.error('函数调用失败');
    }
  };

  // 删除函数
  const handleDelete = async (name) => {
    try {
      await lambdaService.deleteFunction(name);
      message.success('函数删除成功');
      fetchFunctions();
    } catch (error) {
      message.error('函数删除失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '运行时',
      dataIndex: 'runtime',
      key: 'runtime',
    },
    {
      title: '内存',
      dataIndex: 'memory',
      key: 'memory',
    },
    {
      title: '超时时间',
      dataIndex: 'timeout',
      key: 'timeout',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={() => handleInvoke(record.name)}
          >
            调用
          </Button>
          <Popconfirm
            title="确定要删除这个函数吗？"
            onConfirm={() => handleDelete(record.name)}
            okText="确定"
            cancelText="取消"
          >
            <Button icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '16px' }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setModalVisible(true)}
        >
          部署函数
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={functions}
        loading={loading}
        rowKey="name"
      />

      <Modal
        title="部署函数"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleDeploy}
        >
          <Form.Item
            name="name"
            label="函数名称"
            rules={[{ required: true, message: '请输入函数名称' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="runtime"
            label="运行时"
            rules={[{ required: true, message: '请选择运行时' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="handler"
            label="处理函数"
            rules={[{ required: true, message: '请输入处理函数' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="code"
            label="函数代码"
            rules={[{ required: true, message: '请输入函数代码' }]}
          >
            <Input.TextArea rows={10} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">
              部署
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default LambdaPage; 