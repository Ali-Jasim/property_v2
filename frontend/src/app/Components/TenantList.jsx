import React, { useState, useEffect } from "react";
import {
  Container,
  ListGroup,
  Form,
  Button,
  InputGroup,
  Alert,
  Card,
  Modal,
  Spinner,
} from "react-bootstrap";

const TenantList = () => {
  const [tenants, setTenants] = useState([]);
  const [newTenantName, setNewTenantName] = useState("");
  const [newTenantPhone, setNewTenantPhone] = useState("");
  const [newTenantEmail, setNewTenantEmail] = useState("");
  const [newTenantLandlordId, setNewTenantLandlordId] = useState("");
  const [editTenant, setEditTenant] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch tenants on component mount
  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/tenants/", {
        method: "GET",
        mode: "cors",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Fetched tenants:", data);
      setTenants(data);
      setError(null);
    } catch (err) {
      console.error("Error fetching tenants:", err);
      setError("Failed to load tenants. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      newTenantName.trim() === "" ||
      newTenantPhone.trim() === "" ||
      newTenantEmail.trim() === "" ||
      newTenantLandlordId.trim() === ""
    )
      return;

    try {
      // Create URL with query parameters
      const url = new URL("http://localhost:8000/tenants/");
      url.searchParams.append("name", newTenantName.trim());
      url.searchParams.append("phone_number", newTenantPhone.trim());
      url.searchParams.append("email", newTenantEmail.trim());
      url.searchParams.append("landlord_id", newTenantLandlordId.trim());

      console.log("Sending request to:", url.toString());

      const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const newTenant = await response.json();
      setTenants([...tenants, newTenant]);
      setNewTenantName("");
      setNewTenantPhone("");
      setNewTenantEmail("");
      setNewTenantLandlordId("");
      setShowCreate(false);
      setError(null);
    } catch (err) {
      console.error("Error creating tenant:", err);
      setError("Failed to create tenant. Please try again.");
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/tenants/${id}`, {
        method: "DELETE",
        mode: "cors",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      setTenants(tenants.filter((tenant) => tenant.id !== id));
      setError(null);
    } catch (err) {
      console.error("Error deleting tenant:", err);
      setError("Failed to delete tenant. Please try again.");
    }
  };

  const handleEdit = (tenant) => {
    setEditTenant(tenant);
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      const url = new URL(`http://localhost:8000/tenants/${editTenant.id}`);
      url.searchParams.append("name", editTenant.name);
      url.searchParams.append("phone_number", editTenant.phone_number);
      url.searchParams.append("email", editTenant.email);
      url.searchParams.append("landlord_id", editTenant.landlord_id);

      const response = await fetch(url, {
        method: "PUT",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const updatedTenant = await response.json();
      setTenants(
        tenants.map((tenant) =>
          tenant.id === editTenant.id ? updatedTenant : tenant
        )
      );
      setShowModal(false);
      setEditTenant(null);
      setError(null);
    } catch (err) {
      console.error("Error updating tenant:", err);
      setError("Failed to update tenant. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="tenant-list">
        <Card.Header>Tenant List</Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}

          {loading ? (
            <div className="text-center">
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : tenants.length === 0 ? (
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
                    <div>{tenant.phone_number}</div>
                    <div>{tenant.email}</div>
                    <div>{tenant.landlord_id}</div>
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
          <Button
            variant="secondary"
            onClick={() => setShowCreate(!showCreate)}
          >
            {showCreate ? "Cancel" : "Create"}
          </Button>
          {showCreate && (
            <Form onSubmit={handleSubmit} className="mb-4 mt-3">
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
                  value={newTenantPhone}
                  onChange={(e) => setNewTenantPhone(e.target.value)}
                  placeholder="Enter tenant phone"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="email"
                  value={newTenantEmail}
                  onChange={(e) => setNewTenantEmail(e.target.value)}
                  placeholder="Enter tenant email"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newTenantLandlordId}
                  onChange={(e) => setNewTenantLandlordId(e.target.value)}
                  placeholder="Enter landlord ID"
                />
              </InputGroup>
              <Button variant="primary" type="submit">
                Add Tenant
              </Button>
            </Form>
          )}
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
                value={editTenant?.phone_number || ""}
                onChange={(e) =>
                  setEditTenant({ ...editTenant, phone_number: e.target.value })
                }
                placeholder="Enter tenant phone"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="email"
                value={editTenant?.email || ""}
                onChange={(e) =>
                  setEditTenant({ ...editTenant, email: e.target.value })
                }
                placeholder="Enter tenant email"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editTenant?.landlord_id || ""}
                onChange={(e) =>
                  setEditTenant({
                    ...editTenant,
                    landlord_id: e.target.value,
                  })
                }
                placeholder="Enter landlord ID"
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
