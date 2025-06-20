-- 1. Critical Service Terminology (Highest Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Pallets', 'Could you please confirm the total number of pallets involved?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Frozen pallets', 'Please ensure the frozen pallets are kept at the required temperature before collection.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Chilled pallets', 'Have the chilled pallets been prepared for pickup and stored appropriately?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Half-filled pallets', 'Can we consolidate the half-filled pallets to optimize space?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Full pallets', 'Thank you for confirming these are full pallets. We''ll arrange transport accordingly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Stacked pallets', 'Are the pallets securely stacked and shrink-wrapped for safe loading?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Damaged pallets', 'Could you share photos of the damaged pallets so we can assess the condition?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Empty pallets', 'Would you like us to collect the empty pallets together with the other items?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Pending pallets', 'Noted on the pending pallets --- please update us once they are ready.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'PO#', 'May I have the PO number for this batch so we can proceed with verification?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'PO verification', 'We are currently verifying the PO. Will update you shortly once it''s cleared.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'PO list', 'Kindly share the PO list so we can cross-check with the items for pickup.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'PO amendment', 'If there''s an amendment to the PO, please send us the updated version.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'PO confirmation', 'We''ve received the PO and will proceed after your final confirmation.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Container number', 'Could you confirm the container number for tracking and clearance purposes?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Customs clearance', 'We are currently arranging customs clearance. Please ensure all documents are ready.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Container tracking', 'We will share the tracking update once the container is dispatched.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Container seal', 'Please check that the container seal is intact before collection.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Container capacity', 'Can you advise on the remaining capacity of the container for load planning?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal', 'We''ve scheduled the disposal for [day/time]. Please ensure items are ready.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal certificate', 'The disposal certificate and report will be issued post-processing.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal video', 'We will share the disposal video and photos after completion for your records.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal cost', 'We''ll send the disposal cost breakdown together with the invoice.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal confirmation', 'The disposal has been completed. Confirmation and documentation will follow.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Disposal delay', 'Apologies for the delay --- we''re working to reschedule the disposal at the earliest.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Invoice', 'The invoice (No. [####]) has been issued. Kindly confirm receipt.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Invoice verification', 'We are verifying the invoice details and will revert shortly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Invoice amendment', 'Please advise if you require any amendments before we finalize the invoice.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Invoice payment', 'May I know the expected payment date for the pending invoice?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Invoice attachment', 'Kindly refer to the attached invoice for your review.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Safety Gear', 'Please ensure all personnel are equipped with proper safety gear and follow compliance protocols during the collection.', 20);

-- 2. Time and Date-Related Keywords (High Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Collection Time', 'Please confirm the collection time so we can coordinate with our team.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'ETA', 'Could you share the latest ETA for the shipment?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Delay', 'We''re aware of the delay and will update the revised timing shortly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Early arrival', 'Noted on the early arrival. We''ll ensure the team is ready in advance.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Late arrival', 'Thanks for the heads-up on the delay --- we''ll adjust our schedule accordingly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Collection window', 'Kindly advise your available collection window for scheduling.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Deadline', 'Just a reminder, the deadline is approaching. Please submit the required documents on time.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Extension request', 'Understood --- we''ll review the request for deadline extension and get back to you.', 20);

-- 3. Item and Scene Descriptions (Mid-High Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Frozen Items', 'Please confirm the storage condition for the frozen items prior to dispatch.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Chilled Items', 'Have the chilled goods been packed and stored correctly for delivery?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Expired Items', 'Please send photos of the expired items for our records and disposal process.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Damaged Items', 'Can you provide images of the damaged items so we can proceed with a report?', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Mouldy Items', 'Thanks for the update --- we''ll flag the mouldy goods for disposal and arrange accordingly.', 20);

-- 4. Operational Commands (Medium Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Consolidate', 'We''ll consolidate the pallets to reduce space and optimize handling.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Repack', 'Noted. We''ll proceed with repacking as per your instruction.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Merge shipments', 'Merging the shipments is possible. We''ll confirm space availability.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Attach', 'Please see the attached file for your reference.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Hold', 'The operation is on hold temporarily. We''ll notify once resumed.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Resume', 'The operation has been resumed. Team is aligned.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Verify', 'We''re verifying the details now --- will update you shortly.', 20);

-- 5. Question Keywords (Medium Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'How many?', 'There are a total of [XX] units confirmed for this delivery.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'When?', 'The event is scheduled for [date/time].', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Where?', 'The truck is currently at [location]. Loading will take place at Bay [X].', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Why?', 'The delay is due to [reason]. We''re working to resolve it ASAP.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Can you?', 'Yes, we can proceed as requested.', 20);

-- 6. Common Conversational Phrases (Lowest Priority)
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Greetings', 'Good morning! Hope you''re doing well.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Politeness', 'Thanks for your patience. Much appreciated!', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Acknowledgement', 'Noted with thanks. Will follow up accordingly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Wait', 'Give me a moment to check and I''ll get back to you shortly.', 20);
INSERT INTO rules (rule_type, is_builtin, keywords, response, priority) VALUES ('keyword', 1, 'Apologies', 'Apologies for the delay and any inconvenience caused.', 20);