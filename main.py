import cryo
from eth_abi import decode, encode
from src.helpers import hexstr_to_bytes, bytes_to_hexstr

UNIV2_WETH_USDC = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"

GET_RESERVES_4b = hexstr_to_bytes("0x0902f1ac")

if __name__ == "__main__":
    # Multicall3 encoded calldasta
    df = cryo.collect(
        "eth_calls",
        include_columns=(["block_number", "output_data"]),
        to_address=[UNIV2_WETH_USDC],
        call_data=[bytes_to_hexstr(GET_RESERVES_4b)],
        label="exchange_rate",
        output_format="polars",
        blocks=["-5:latest"],
        no_verbose=True,
        rpc="https://eth.merkle.io",
    )

    # Get the output data
    for cur_row in df.sort('block_number').to_dicts():
        output_data = cur_row['output_data']
        block_number = cur_row['block_number']

        if output_data is None or len(output_data) == 0:
            continue

        # Get reserve numbers
        [usdc_reserve, weth_reserve, _] = decode(
            ["(uint112,uint112,uint32)"], output_data
        )[0]
        weth_usdc = (usdc_reserve / 1e6) / (weth_reserve / 1e18)

        print(block_number, weth_usdc)
