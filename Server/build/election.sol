// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract Election {
    address public manager;
    uint256 public totalVoter;
    uint256 public totalCandidate;
    uint256 public voteDropped;

    enum State {Created, Voting, Ended}
    State public state;

    struct Voter {
        address voterAddress;
        bool isVoter;
        bool voted;
    }

    struct Candidate {
        address candidateAddress;
        bool isCandidate;
        uint256 totalVoteCount;
    }

    mapping(address => Voter) public voters;
    mapping(address => Candidate) public candidates;
    address[] public candidateAddresses;

    constructor() {
        manager = msg.sender;
        state = State.Created;
        totalVoter = 0;
        totalCandidate = 0;
        voteDropped = 0;
        addVoter(msg.sender);
    }

    modifier onlyManager() {
        require(msg.sender == manager, "Manager only has persmission.");
        _;
    }

    modifier inState(State _state) {
        require(state == _state, "Election phase restriction.");
        _;
    }

    modifier notVoted() {
        require(
            voters[msg.sender].voted == false,
            "The voter who has not voted can cast vote."
        );
        _;
    }

    modifier isVoter() {
        require(voters[msg.sender].isVoter, "User must be voter.");
        _;
    }

    event voterAdded(address _voter);
    event candidateAdded(address _candidate);
    event voteStarted();
    event voteDone(address voter);
    event voteEnded();
    event electionResult(address _candidate);

    function addVoter(address _voterAddress)
        public
        inState(State.Created)
        onlyManager
        returns (address)
    {
        require(!voters[_voterAddress].isVoter, "Voter already registered.");
        voters[_voterAddress] = Voter({
            voterAddress: _voterAddress,
            isVoter: true,
            voted: false
        });

        totalVoter++;

        emit voterAdded(_voterAddress);
        return voters[_voterAddress].voterAddress;
    }
    
    function removeVoter(address _voterAddress)
        public
        inState(State.Created)
        onlyManager
        returns (bool)
        {
            require(voters[_voterAddress].isVoter, "Voter not exist.");
            delete voters[_voterAddress];
            if (candidates[_voterAddress].isCandidate){
                delete candidates[_voterAddress];
            }
            return true;
        }

    function addCandidate(address _candidateAddress)
        public
        inState(State.Created)
        onlyManager
        returns (address)
    {
        require(!candidates[_candidateAddress].isCandidate, "Candidate already registered.");
        candidates[_candidateAddress] = Candidate({
            candidateAddress: _candidateAddress,
            totalVoteCount: 0,
            isCandidate: true
        });
        candidateAddresses.push(_candidateAddress);
        
        if (!voters[_candidateAddress].isVoter){
            addVoter(_candidateAddress);
        }
        
        totalCandidate++;
        emit candidateAdded(_candidateAddress);
        
        return candidates[_candidateAddress].candidateAddress;
    }
    
    function startVote() public inState(State.Created) onlyManager {
        state = State.Voting;
        emit voteStarted();
    }

    function doVote(address _candidateAddress)
        public
        inState(State.Voting)
        notVoted
        isVoter
    {
        require(candidates[_candidateAddress].isCandidate, "User must be candidate");

        voters[msg.sender].voted = true;
        candidates[_candidateAddress].totalVoteCount++;

        voteDropped++;

        emit voteDone(msg.sender);
    }

    function endVote()
        public
        inState(State.Voting)
        onlyManager
        returns (uint256)
    {
        state = State.Ended;
        emit voteEnded();
        return voteDropped;
    }
    
    function result()
        public
        inState(State.Ended)
        onlyManager
        returns(address)
    {
        address winner;
        uint winningVoteCount = 0;
        for (uint p = 0; p < candidateAddresses.length; p++) {
            if (candidates[candidateAddresses[p]].totalVoteCount > winningVoteCount) 
            {
                winningVoteCount = candidates[candidateAddresses[p]].totalVoteCount;
                winner = candidateAddresses[p];
            }
        }
        emit electionResult(winner);
        return winner;
    }
}
