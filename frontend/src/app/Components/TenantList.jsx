import React, { useState } from "react";
import {
  Container,
  ListGroup,
  Form,
  Button,
  InputGroup,
  Alert,
  Card,
  Modal,
} from "react-bootstrap";

const TenantList = () => {
  const [tenants, setTenants] = useState([]);
  const [newTenantName, setNewTenantName] = useState("");
  const [newTenantAddress, setNewTenantAddress] = useState("");
  const [editTenant, setEditTenant] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newTenantName.trim() === "" || newTenantAddress.trim() === "") return;

    setTenants([
      ...tenants,
      {
        id: Date.now(),
        name: newTenantName.trim(),
        address: newTenantAddress.trim(),
      },
    ]);
    setNewTenantName("");
    setNewTenantAddress("");
  };

  const handleDelete = (id) => {
    setTenants(tenants.filter((tenant) => tenant.id !== id));
  };

  const handleEdit = (tenant) => {
    setEditTenant(tenant);
    setShowModal(true);
  };

  const handleSave = () => {
    setTenants(
      tenants.map((tenant) =>
        tenant.id === editTenant.id ? editTenant : tenant
      )
    );
    setShowModal(false);
    setEditTenant(null);
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="tenant-list">
        <Card.Header>Tenant List</Card.Header>
        <Card.Body>
          {tenants.length === 0 ? (
            <Alert variant="info">No tenants in the list yet!</Alert>
          ) : (
            <ListGroup>
              {tenants.map((tenant) => (
                <ListGroup.Item
                  key={tenant.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>{tenant.name}</div>
                    <div>{tenant.address}</div>
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleEdit(tenant)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(tenant.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
          <br />
          <Form onSubmit={handleSubmit} className="mb-4">
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newTenantName}
                onChange={(e) => setNewTenantName(e.target.value)}
                placeholder="Enter tenant name"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newTenantAddress}
                onChange={(e) => setNewTenantAddress(e.target.value)}
                placeholder="Enter tenant address"
              />
            </InputGroup>
            <Button variant="primary" type="submit">
              Add Tenant
            </Button>
          </Form>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Tenant</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editTenant?.name || ""}
                onChange={(e) =>
                  setEditTenant({ ...editTenant, name: e.target.value })
                }
                placeholder="Enter tenant name"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editTenant?.address || ""}
                onChange={(e) =>
                  setEditTenant({ ...editTenant, address: e.target.value })
                }
                placeholder="Enter tenant address"
              />
            </InputGroup>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default TenantList;
