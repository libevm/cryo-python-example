import cryo
from eth_abi import decode, encode
from src.helpers import hexstr_to_bytes, bytes_to_hexstr

MULTICALL3_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11"

UNIV2_WETH_USDC = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"

TRYAGGREGATE_4b = hexstr_to_bytes("0xbce38bd7")
GET_RESERVES_4b = hexstr_to_bytes("0x0902f1ac")

if __name__ == "__main__":
    # Multicall3 encoded calldasta
    inner_calldata = [[UNIV2_WETH_USDC, GET_RESERVES_4b]]
    m3_calldata_bytes = encode(
        ["bool", "(address,bytes)[]"], [False, inner_calldata]
    )
    m3_calldata = bytes_to_hexstr(TRYAGGREGATE_4b + m3_calldata_bytes)

    # Perform eth_call
    df = cryo.collect(
        "eth_calls",
        include_columns=(["block_number", "output_data"]),
        to_address=[MULTICALL3_ADDRESS],
        call_data=[m3_calldata],
        label="exchange_rate",
        output_format="polars",
        blocks=["latest"],
        no_verbose=True,
        rpc="https://eth.merkle.io",
    )

    # Get the output data
    output_data = df['output_data'].to_list()

    for cur_row in df.to_dicts():
        output_data = cur_row['output_data']
        block_number = cur_row['block_number']

        # Decode the data, only care about the return data
        [decoded_data] = decode(["(bool,bytes)[]"], output_data)
        return_data = [x[1] for x in decoded_data]

        # Get reserve numbers
        [usdc_reserve, weth_reserve, _] = decode(
            ["(uint112,uint112,uint32)"], return_data[0]
        )[0]
        weth_usdc = (usdc_reserve / 1e6) / (weth_reserve / 1e18)

        print(block_number, weth_usdc)
