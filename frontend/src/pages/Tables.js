import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { listCompanies } from '../actions/companyActions';
import { Row, Col, Card, Table, Spin, Alert, Typography } from 'antd';
import FeedbackForm from './Feedbackform';
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

const { Title } = Typography;

const columns = (userInfo) => [
  {
    title: "SOFTWARE/WEBSITE",
    dataIndex: "name",
    key: "name",
    width: "32%",
  },
  {
    title: "WEBSITE URL",
    dataIndex: "website",
    key: "website",
  },
  {
    title: "EMAIL",
    key: "email",
    dataIndex: "email",
  },
  {
    title: "CREATED AT",
    key: "createdAt",
    dataIndex: "createdAt",
  },
  {
    title: "ACTION",
    key: "action",
    render: (text, record) => (
      <span>
        {userInfo?.is_normal_user && <FeedbackForm companyId={record.key} userInfo={userInfo} />} {/* Pass userInfo as prop */}
      </span>
    ),
  },
];

function Tables() {
  const dispatch = useDispatch();
  const history = useHistory();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const companyList = useSelector((state) => state.companyList);
  const { loading, error, companies } = companyList;

  useEffect(() => {
    dispatch(listCompanies());
  }, [dispatch]);

 

  return (
    <>
      <div className="tabled">
        <Row gutter={[24, 0]}>
          <Col xs="24" xl={24}>
            <Card
              bordered={false}
              className="criclebox tablespace mb-24"
              title="Registered Websites/ Software"
            >
              {loading ? (
                <Spin />
              ) : error ? (
                <Alert message="Error" description={error} type="error" showIcon />
              ) : (
                <div className="table-responsive">
                  <Table
                    columns={columns(userInfo)} 
                    dataSource={companies.map((company) => ({
                      key: company.id,
                      name: company.name,
                      website: company.website_url,
                      email: company.email,
                      createdAt: company.created_at,
                    }))}
                    pagination={false}
                    className="ant-border-space"
                  />
                </div>
              )}
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Tables;
