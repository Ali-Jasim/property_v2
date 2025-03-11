
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import TenantList from './app/Components/TenantList';
import ContractorList from './app/Components/ContractorList';
import { Row, Col, Navbar } from 'react-bootstrap';
import IssueList from './app/Components/IssueList';
import PropertyList from './app/Components/PropertyList';





function App() {
  return (
    <div className="main-container">

      <Navbar bg="dark" variant="dark" className='navbar'>
        <Navbar.Brand href="#home">Property Management</Navbar.Brand>
      </Navbar>


      <Row className="main-content">
        <Col lg={4} md={12} className='test'>
          <TenantList />
        </Col>
        <Col lg={4} md={12}>
          <ContractorList />
        </Col>
        <Col lg={4} md={12} >
          <PropertyList />
        </Col>
        <Col lg={4} md={12}>
          <IssueList />
        </Col>
      </Row>
    </div>
  );
}

export default App;
