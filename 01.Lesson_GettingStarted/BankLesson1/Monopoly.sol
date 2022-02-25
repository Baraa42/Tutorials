pragma solidity 0.8.12;

contract Monopoly {
    bytes8 public FACTOR = 0x000000012ACE4C7F;
    uint256 public landPrice = 0.3 gwei;
    uint32 private last = type(uint32).max - 3;
    uint256 public balance;
    mapping(address => uint32) lastMove;

    function roll(uint32 _seed) internal returns (uint16) {
        uint16 dice;
        if (uint64(FACTOR) % _seed == 0) {
            unchecked {
                dice =
                    uint16(_seed) ^
                    uint16(bytes2(bytes20(address(msg.sender)))); // 0x d8 b9
            }
        } else {
            unchecked {
                dice =
                    uint16(_seed) ^
                    uint16(
                        bytes2(
                            bytes20(
                                address(
                                    0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
                                )
                            )
                        )
                    );
            }
        }
        assert(dice != 0);
        return dice;
    }

    // (
    //             _index == last / 4 + 1 ||
    //             _index == (last / 4) * 2 + 2 ||
    //             _index == (last / 4) * 3 + 3
    //         )
}
