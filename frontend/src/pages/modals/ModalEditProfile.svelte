<script>
    import {
        Button,
        Modal,
        ModalBody,
        ModalFooter,
        ModalHeader,
        Form,
        FormGroup,
        Label,
        Input,
    } from "sveltestrap";
    import { update_user_by_id } from "../../helpers/http_requests";
    import { show_toaster } from "../../helpers/alerts";
    import { user as userStore } from "../../helpers/stores";

    // props
    export let user = "";
    let temp_user;

    // modal config
    let edit_profile_open = false;
    let size = "md";

    export const open_edit_profile = async () => {
        edit_profile_open = !edit_profile_open;
        if (edit_profile_open) {
            temp_user = JSON.parse(JSON.stringify(user));
        } else {
            temp_user = "";
        }
    };

    const update_profile = async (new_user) => {
        try {
            let updated_user = {
                firstname: new_user.firstname,
                lastname: new_user.lastname,
                username: new_user.username,
                email: new_user.email,
                phone: new_user.phone,
                password: "",
            };

            const resp = await update_user_by_id(updated_user, new_user._id);
            if (resp.ok) {
                const updatedData = await resp.json();
                $userStore = updatedData;
                show_toaster("success", "Profile updated successfully");
                open_edit_profile();
            } else {
                const error = await resp.json();
                show_toaster(
                    "error",
                    error.detail || "Failed to update profile",
                );
            }
        } catch (error) {
            show_toaster("error", "An error occurred while updating profile");
        }
    };

    const save_changes = () => {
        update_profile(temp_user);
    };
</script>

<Modal isOpen={edit_profile_open} {open_edit_profile} {size} scrollable>
    <ModalHeader {open_edit_profile}>Editing Profile</ModalHeader>
    <ModalBody>
        <Form>
            <FormGroup>
                <Label>First Name</Label>
                <Input type="text" bind:value={temp_user.firstname} />
            </FormGroup>
            <FormGroup>
                <Label>Last Name</Label>
                <Input type="text" bind:value={temp_user.lastname} />
            </FormGroup>
            <FormGroup>
                <Label>Email</Label>
                <Input type="email" bind:value={temp_user.email} />
            </FormGroup>
            <FormGroup>
                <Label>Phone</Label>
                <Input type="tel" bind:value={temp_user.phone} />
            </FormGroup>
        </Form>
    </ModalBody>
    <ModalFooter>
        <Button color="danger" on:click={open_edit_profile}>Cancel</Button>
        <Button color="primary" on:click={save_changes}>Save Changes</Button>
    </ModalFooter>
</Modal>

<style>
    :global(.modal-content) {
        border-radius: var(--border-radius-lg);
    }

    :global(.form-label) {
        color: var(--text-secondary);
        font-weight: 500;
    }

    :global(.form-control) {
        border-color: var(--border-color);
    }

    :global(.form-control:focus) {
        border-color: var(--secondary);
        box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25);
    }
</style>
