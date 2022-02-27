# Properties For Spartan



1. ***Valid state*** - `balance(e)` <= `total()`.

2. ***Variable transition*** - `token0Amount` and `token1Amount` increase in the same time only when add_liquidity or init_pool is called.

3. ***Variable transition*** - `token0Amount` and `token1Amount` decrease in the same time only when remove_liquidity is called.

4. ***Variable transition*** - `token0Amount` and `token1Amount` change in opposite directions only when swap is called.

5. ***Variable transition*** - `K` increase  only when add_liquidity  or init_pool is called.

6. ***Variable transition*** - `K` decrease  only when remove_liquidity  or init_pool is called.

7. ***Variable transition*** - `K` doesn't change   when swap   is called.

9. ***Unit tests*** - add_liquidity() correctly changes `token0Amount` and `token1Amount` and `K`.

10. ***Unit tests*** - remove_liquidity() correctly changes `token0Amount` and `token1Amount` and `K`.




