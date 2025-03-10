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

const ContractorList = () => {
  const [contractors, setContractors] = useState([]);
  const [newContractorName, setNewContractorName] = useState("");
  const [newContractorEmail, setNewContractorEmail] = useState("");
  const [newContractorPhone, setNewContractorPhone] = useState("");
  const [newContractorWork, setNewContractorWork] = useState("");
  const [editContractor, setEditContractor] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (
      newContractorName.trim() === "" ||
      newContractorEmail.trim() === "" ||
      newContractorPhone.trim() === "" ||
      newContractorWork.trim() === ""
    )
      return;

    setContractors([
      ...contractors,
      {
        id: Date.now(),
        name: newContractorName.trim(),
        email: newContractorEmail.trim(),
        phone: newContractorPhone.trim(),
        work: newContractorWork.trim(),
      },
    ]);
    setNewContractorName("");
    setNewContractorEmail("");
    setNewContractorPhone("");
    setNewContractorWork("");
  };

  const handleDelete = (id) => {
    setContractors(contractors.filter((contractor) => contractor.id !== id));
  };

  const handleEdit = (contractor) => {
    setEditContractor(contractor);
    setShowModal(true);
  };

  const handleSave = () => {
    setContractors(
      contractors.map((contractor) =>
        contractor.id === editContractor.id ? editContractor : contractor
      )
    );
    setShowModal(false);
    setEditContractor(null);
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="contractor-list">
        <Card.Header>Contractor List</Card.Header>
        <Card.Body>
          {contractors.length === 0 ? (
            <Alert variant="info">No contractors in the list yet!</Alert>
          ) : (
            <ListGroup>
              {contractors.map((contractor) => (
                <ListGroup.Item
                  key={contractor.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>{contractor.name}</div>
                    <div>{contractor.email}</div>
                    <div>{contractor.phone}</div>
                    <div>{contractor.work}</div>
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleEdit(contractor)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(contractor.id)}
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
                value={newContractorName}
                onChange={(e) => setNewContractorName(e.target.value)}
                placeholder="Enter contractor name"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="email"
                value={newContractorEmail}
                onChange={(e) => setNewContractorEmail(e.target.value)}
                placeholder="Enter contractor email"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newContractorPhone}
                onChange={(e) => setNewContractorPhone(e.target.value)}
                placeholder="Enter contractor phone"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newContractorWork}
                onChange={(e) => setNewContractorWork(e.target.value)}
                placeholder="Enter contractor work"
              />
            </InputGroup>
            <Button variant="primary" type="submit">
              Add Contractor
            </Button>
          </Form>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Contractor</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.name || ""}
                onChange={(e) =>
                  setEditContractor({ ...editContractor, name: e.target.value })
                }
                placeholder="Enter contractor name"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="email"
                value={editContractor?.email || ""}
                onChange={(e) =>
                  setEditContractor({
                    ...editContractor,
                    email: e.target.value,
                  })
                }
                placeholder="Enter contractor email"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.phone || ""}
                onChange={(e) =>
                  setEditContractor({
                    ...editContractor,
                    phone: e.target.value,
                  })
                }
                placeholder="Enter contractor phone"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.work || ""}
                onChange={(e) =>
                  setEditContractor({ ...editContractor, work: e.target.value })
                }
                placeholder="Enter contractor work"
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

export default ContractorList;
