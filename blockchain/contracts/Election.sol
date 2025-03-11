// SPDX-License-Identifier: MIT
pragma solidity >=0.5.2;

contract Election {
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    struct Voter {
        uint256 id;
        string name;
        bool hasVoted;
    }

    struct ElectionData {
        uint256 id;
        string name;
        mapping(uint256 => Candidate) candidates;
        mapping(uint256 => Voter) voters;
        uint256 candidatesCount;
        uint256 voterCount;
    }

    mapping(uint256 => ElectionData) public elections;
    uint256 public electionsCount;

    event ElectionCreated(uint256 indexed electionId, string name);
    event CandidateAdded(uint256 indexed electionId, uint256 candidateId, string name);
    event VoterAdded(uint256 indexed electionId, uint256 voterId, string name);
    event VoteCast(uint256 indexed electionId, uint256 candidateId);

    function createElection(string memory _name) public {
        electionsCount++;
        elections[electionsCount].id = electionsCount;
        elections[electionsCount].name = _name;
        emit ElectionCreated(electionsCount, _name);
    }

    function addCandidate(uint256 _electionId, uint256 _id, string memory _name) public {
        ElectionData storage election = elections[_electionId];
        election.candidatesCount++;
        election.candidates[election.candidatesCount] = Candidate(_id, _name, 0);
        emit CandidateAdded(_electionId, _id, _name);
    }

    function addVoter(uint256 _electionId, uint256 _id, string memory _name) public {
        ElectionData storage election = elections[_electionId];
        election.voterCount++;
        election.voters[election.voterCount] = Voter(_id, _name, false);
        emit VoterAdded(_electionId, _id, _name);
    }

    function vote(uint256 _electionId, uint256 _candidateId, uint256 _voterId) public {
        ElectionData storage election = elections[_electionId];
        require(!election.voters[_voterId].hasVoted, "Voter has already voted");
        election.voters[_voterId].hasVoted = true;
        election.candidates[_candidateId].voteCount++;
        emit VoteCast(_electionId, _candidateId);
    }

    function getResults(uint256 _electionId) public view returns (uint256[] memory, string[] memory, uint256[] memory) {
        ElectionData storage election = elections[_electionId];
        uint256[] memory ids = new uint256[](election.candidatesCount);
        string[] memory names = new string[](election.candidatesCount);
        uint256[] memory votes = new uint256[](election.candidatesCount);
        
        for (uint256 i = 1; i <= election.candidatesCount; i++) {
            ids[i - 1] = election.candidates[i].id;
            names[i - 1] = election.candidates[i].name;
            votes[i - 1] = election.candidates[i].voteCount;
        }
        return (ids, names, votes);
    }
}
