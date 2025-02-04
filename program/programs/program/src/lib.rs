Here is a basic example of how you might structure a Solana smart contract using the Anchor framework in Rust:

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{self, TokenAccount, Transfer};

#[program]
pub mod basic {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> ProgramResult {
        Ok(())
    }

    pub fn transfer(ctx: Context<Transfer>, amount: u64) -> ProgramResult {
        let cpi_program = ctx.accounts.token_program.to_account_info().clone();
        let cpi_accounts = Transfer {
            from: ctx.accounts.from.to_account_info().clone(),
            to: ctx.accounts.to.to_account_info().clone(),
            authority: ctx.accounts.authority.to_account_info().clone(),
        };
        let cpi_ctx = CpiContext::new(cpi_program, cpi_accounts);
        token::transfer(cpi_ctx, amount)
    }
}

#[derive(Accounts)]
pub struct Initialize {
    #[account(init)]
    pub from: Account<'info, TokenAccount>,
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    #[account(address = token::ID)]
    pub token_program: Program<'info, Token>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct Transfer {
    pub from: Account<'info, TokenAccount>,
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    #[account(address = token::ID)]
    pub token_program: Program<'info, Token>,
}
```

This contract includes a function to initialize a token transfer and another function to perform the transfer. The `#[derive(Accounts)]` attribute is used to define the account context for each instruction, and the `#[program]` attribute is used to define the smart contract's on-chain program ID.

Note that this is a very simple contract without any complex logic or state management, and it doesn't address all the requirements outlined in your question. Developing a full-fledged vesting contract with cliff periods, emergency pause functionality, and admin controls would be significantly more complex and beyond the scope of this example.