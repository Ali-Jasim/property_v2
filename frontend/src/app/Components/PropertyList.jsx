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

const PropertyList = () => {
  const [properties, setProperties] = useState([]);
  const [newPropertyAddress, setNewPropertyAddress] = useState("");
  const [newPropertyLandlordId, setNewPropertyLandlordId] = useState("");
  const [editProperty, setEditProperty] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newPropertyAddress.trim() === "" || newPropertyLandlordId.trim() === "")
      return;

    setProperties([
      ...properties,
      {
        id: Date.now(),
        address: newPropertyAddress.trim(),
        landlord_id: newPropertyLandlordId.trim(),
      },
    ]);
    setNewPropertyAddress("");
    setNewPropertyLandlordId("");
    setShowCreate(false);
  };

  const handleDelete = (id) => {
    setProperties(properties.filter((property) => property.id !== id));
  };

  const handleEdit = (property) => {
    setEditProperty(property);
    setShowModal(true);
  };

  const handleSave = () => {
    setProperties(
      properties.map((property) =>
        property.id === editProperty.id ? editProperty : property
      )
    );
    setShowModal(false);
    setEditProperty(null);
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="property-list">
        <Card.Header>Property List</Card.Header>
        <Card.Body>
          {properties.length === 0 ? (
            <Alert variant="info">No properties in the list yet!</Alert>
          ) : (
            <ListGroup>
              {properties.map((property) => (
                <ListGroup.Item
                  key={property.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>Address: {property.address}</div>
                    <div>Landlord ID: {property.landlord_id}</div>
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleEdit(property)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(property.id)}
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
                  value={newPropertyAddress}
                  onChange={(e) => setNewPropertyAddress(e.target.value)}
                  placeholder="Enter property address"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newPropertyLandlordId}
                  onChange={(e) => setNewPropertyLandlordId(e.target.value)}
                  placeholder="Enter landlord ID"
                />
              </InputGroup>
              <Button variant="primary" type="submit">
                Add Property
              </Button>
            </Form>
          )}
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Property</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editProperty?.address || ""}
                onChange={(e) =>
                  setEditProperty({
                    ...editProperty,
                    address: e.target.value,
                  })
                }
                placeholder="Enter property address"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editProperty?.landlord_id || ""}
                onChange={(e) =>
                  setEditProperty({
                    ...editProperty,
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

export default PropertyList;
