import React, { useEffect, useState } from "react";
import { ethers } from "ethers";
import { Button, Card, Select } from "@/components/ui";

const CONTRACT_ADDRESS = "<YOUR_CONTRACT_ADDRESS>";
const CONTRACT_ABI = [
  // Replace with your actual contract ABI
];

const VotingDApp = () => {
  const [elections, setElections] = useState([]);
  const [selectedElection, setSelectedElection] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [account, setAccount] = useState(null);

  useEffect(() => {
    connectWallet();
    fetchElections();
  }, []);

  const connectWallet = async () => {
    if (window.ethereum) {
      const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
      setAccount(accounts[0]);
    } else {
      alert("MetaMask is required");
    }
  };

  const fetchElections = async () => {
    if (!window.ethereum) return;
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
    const electionsList = await contract.getElections();
    setElections(electionsList);
    if (electionsList.length > 0) {
      setSelectedElection(electionsList[0].id);
      fetchCandidates(electionsList[0].id);
    }
  };

  const fetchCandidates = async (electionId) => {
    if (!window.ethereum) return;
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
    const candidatesList = await contract.getResults(electionId);
    setCandidates(candidatesList);
  };

  const vote = async (electionId, candidateId) => {
    if (!window.ethereum) return;
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);
    await contract.vote(electionId, candidateId);
    alert("Vote cast successfully!");
    fetchCandidates(electionId);
  };

  return (
    <div className="p-5">
      <h1 className="text-2xl font-bold">Decentralized Voting DApp</h1>
      <p>Connected Account: {account || "Not connected"}</p>
      <Button onClick={connectWallet}>Connect Wallet</Button>
      <div className="mt-4">
        <label>Select Election:</label>
        <Select value={selectedElection} onChange={(e) => {
          setSelectedElection(e.target.value);
          fetchCandidates(e.target.value);
        }}>
          {elections.map((election) => (
            <option key={election.id} value={election.id}>{election.name}</option>
          ))}
        </Select>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {candidates.map((candidate, index) => (
          <Card key={index}>
            <h2 className="text-xl font-semibold">{candidate.name}</h2>
            <p>Votes: {candidate.voteCount.toString()}</p>
            <Button onClick={() => vote(selectedElection, candidate.id)}>Vote</Button>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default VotingDApp;
